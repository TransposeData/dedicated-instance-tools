import sys
import time
from datetime import datetime
from typing import Callable

from transpose.common.constants import (
    INDEXER_TABLE_PAGINATED_QUERY,
    OWNER_TABLE_PAGINATED_QUERY,
    TRANSFER_TABLE_PAGINATED_QUERY,
)
from transpose.common.exceptions import InvalidSyncTableError
from transpose.util.io import load_json_from_file, write_json_to_file
from transpose.util.log import get_logger
from transpose.util.threading import TaskPool
from transpose.util.time import estimate_eta


class SyncClient:
    def __init__(self, base_class) -> None:
        self.super = base_class
        self.logger = get_logger("SYNC", self.super.debug)
        self.metadata: dict = {}

    def run(
        self,
        callable: Callable[[list[dict]], None],
        table: str,
        batch_size: int = 100_000,
    ) -> None:
        """
        Runs a sync operation on the given table, pulling all rows from the dedicated instance and passing them to the given callable.

        :param callable: The callable to pass rows to. This callable should accept a list of rows as it's only argument.
        :param table: The table to sync.
        :param batch_size: The number of rows to pull per batch.
        :param limit: The maximum number of rows to pull.
        """

        while True:
            try:
                # pull a batch of rows
                rows = self.__pull_batch(table, batch_size)

                # if there are no rows, we're done
                if not rows:
                    break

                # pass the rows to the given callable
                callable(rows)
            except KeyboardInterrupt:
                sys.exit()

    def save_metadata(self, path: str = "metadata.json") -> None:
        """
        Saves the current metadata to the given path.

        :param path: The path to save the metadata to.
        """
        write_json_to_file(self.metadata, path)

    def load_metadata(self, path: str = "metadata.json") -> None:
        """
        Loads the metadata from the given path.

        :param path: The path to load the metadata from.
        """
        self.metadata = load_json_from_file(path)

    def _classify_table(self, table: str) -> str:
        """
        Classifies the given table based on it's internal schema.

        There are essentially three types of tables:
        1. Transfer tables, which can simply be paginated by `activity_id`.
        2. Owner tables, which can be paginated by their underlying transfer table's `activity_id`.
        3. Indexer tables, which can only be paginated by `__indexer_id` and `__block_number`.

        :param table: The table to classify.
        :return: The classification of the table.
        """

        # fetch the table's schema
        columns = self.super.fetch_schema(table)

        # check if this is an indexer table
        if "__indexer_id" in columns and "__block_number" in columns:
            return "indexer"

        # check if this is an owner table
        elif "owner_address" in columns:
            return "owner"

        elif (
            "activity_id" in columns
            and "from_address" in columns
            and "to_address" in columns
        ):
            return "transfer"

        raise InvalidSyncTableError(
            f"The given table ({table}) does not fall into any of the three sync categories."
        )

    def __fetch_indexer_ids(self, table: str) -> list[str]:
        """
        Returns a list of `_indexer_id`s within the given table.

        :param table: The table to fetch `_indexer_id`s from.
        :return: A list of `_indexer_id`s.
        """

        return [
            str(row["__indexer_id"])
            for row in self.super._execute(
                "SELECT DISTINCT(__indexer_id) FROM {};".format(table)
            )
        ]

    def __pull_indexer_batch(
        self, table: str, batch_size: int, indexer_id: str, progress: int
    ) -> list[dict]:
        """
        Pulls a batch of rows from an indexer table on the dedicated instance.

        :param table: The table to pull rows from.
        :param batch_size: The number of rows to pull.
        :param indexer_id: The indexer id to pull rows for.
        :param progress: The offset to start pulling rows from.
        :return: A list of rows.
        """
        indexer_rows = self.super._execute(
            INDEXER_TABLE_PAGINATED_QUERY.format(table),
            (indexer_id, progress, batch_size),
        )

        # get the highest block number from the rows
        highest_block_number = max([row["__block_number"] for row in indexer_rows])

        # remove rows with the highest block number. this is to prevent duplicate rows from being pulled
        indexer_rows = [
            row for row in indexer_rows if row["__block_number"] < highest_block_number
        ]

        # now, update the progress
        self.metadata["indexer_ids"][indexer_id] = highest_block_number

        self.logger.debug(
            "{} | Progress {}".format(
                indexer_id, self.metadata["indexer_ids"][indexer_id]
            )
        )

        return indexer_rows

    def __pull_batch(self, table: str, batch_size: int) -> list[dict]:
        """
        Pulls a batch of rows from the dedicated instance. Automatically chooses the best sync method to use based on `self.table`'s schema.

        :param table: The table to pull rows from.
        :param batch_size: The number of rows to pull.
        :return: A list of rows.
        """

        # get the table's schema using psycopg2
        classification = self._classify_table(table)

        if classification == "transfer":
            # if the table is a transfer table, we can simply paginate by `activity_id`
            offset = self.metadata.get(classification, 0)

            # fetch the rows
            batch_process_begin_time = time.perf_counter()
            rows = self.super._execute(
                TRANSFER_TABLE_PAGINATED_QUERY.format(table), (offset, batch_size)
            )

            # update the metadata
            maximum_activity_id = max([row["activity_id"] for row in rows])
            self.metadata[classification] = maximum_activity_id

            self.logger.info(
                "{} | {:,.0f} Rows synced in {:.2f}s | Progress {}".format(
                    table,
                    len(rows),
                    time.perf_counter() - batch_process_begin_time,
                    maximum_activity_id,
                )
            )

            return [dict(row) for row in rows]

        elif classification == "owner":
            # if the table is a transfer table, we can simply paginate by `activity_id`
            offset = self.metadata.get(classification, 0)

            # fetch the rows
            batch_process_begin_time = time.perf_counter()
            rows = self.super._execute(
                OWNER_TABLE_PAGINATED_QUERY.format(
                    table, table.replace("_owners", "_transfers")
                ),
                (offset, batch_size),
            )

            # update the metadata
            maximum_activity_id = max([row["activity_id"] for row in rows])
            self.metadata[classification] = maximum_activity_id

            self.logger.info(
                "{} | {:,.0f} Rows synced in {:.2f}s | Progress {}".format(
                    table,
                    len(rows),
                    time.perf_counter() - batch_process_begin_time,
                    maximum_activity_id,
                )
            )

            return [dict(row) for row in rows]

        elif classification == "indexer":
            # get a list of indexer ids from the table. this is slow, so we only do it once every 100 batches
            if (
                self.metadata.get("indexer_ids", None) is None
                or self.metadata.get("batches_till_sync", 100) == 0
            ):
                self.logger.info(f"Fetching new ({table}) indexers from postgres")
                self.metadata["indexer_ids"] = {
                    indexer_id: self.metadata.get("indexer_ids", {}).get(indexer_id, 0)
                    for indexer_id in self.__fetch_indexer_ids(table)
                }
                self.metadata["batches_till_sync"] = 100

            # decrement the batches till sync
            self.metadata["batches_till_sync"] -= 1

            # Create a multiprocessing pool
            batch_process_begin_time = time.perf_counter()
            begin_time = datetime.now()
            pool = TaskPool(
                num_workers=min(32, len(self.metadata["indexer_ids"])), use_threads=True
            )
            targets = [
                (table, batch_size, indexer_id, progress)
                for indexer_id, progress in self.metadata["indexer_ids"].items()
            ]
            results = pool.run(self.__pull_indexer_batch, targets)
            processed_rows = [dict(row) for result in results for row in result]

            self.logger.info(
                "{} | {:,.0f} Rows synced in {:.2f}s | Refreshing indexers in {}".format(
                    table,
                    len(processed_rows),
                    time.perf_counter() - batch_process_begin_time,
                    estimate_eta(
                        begin_time, 100 - self.metadata["batches_till_sync"], 100
                    ),
                )
            )

            return processed_rows
