import sys
from typing import Callable

from transpose.common.constants import (
    OWNER_TABLE_PAGINATED_QUERY,
    TRANSFER_TABLE_PAGINATED_QUERY,
)
from transpose.common.exceptions import InvalidSyncTableError


class SyncClient:
    def __init__(self, base_class) -> None:
        self.super = base_class
        self.logger = self.super.logger
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

        print("SELECT DISTINCT(__indexer_id) FROM {};".format(table))

        return [
            str(row["__indexer_id"])
            for row in self.super._execute(
                "SELECT DISTINCT(__indexer_id) FROM {};".format(table)
            )
        ]

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
            rows = self.super._execute(
                TRANSFER_TABLE_PAGINATED_QUERY, (offset, batch_size)
            )

            # update the metadata
            self.metadata[classification] = offset + batch_size

            return rows

        elif classification == "owner":
            # if the table is a transfer table, we can simply paginate by `activity_id`
            offset = self.metadata.get(classification, 0)

            # fetch the rows
            rows = self.super._execute(
                OWNER_TABLE_PAGINATED_QUERY, (offset, batch_size)
            )

            # update the metadata
            self.metadata[classification] = offset + batch_size

            return rows

        elif classification == "indexer":
            print(1)

            # get a list of indexer ids from the table. this is slow, so we only do it once every 100 batches
            if (
                self.metadata.get("indexer_ids", None) is None
                or self.metadata.get("batches_till_sync", 100) == 0
            ):
                print(2)
                self.metadata["indexer_ids"] = self.__fetch_indexer_ids(table)
                self.metadata["batches_till_sync"] = 100

                print(self.metadata)

            # decrement the batches till sync
            self.metadata["batches_till_sync"] -= 1

            print("running")

            return
