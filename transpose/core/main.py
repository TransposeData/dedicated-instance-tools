import logging
import sys

from psycopg2 import pool as psycopg2_pool
from psycopg2.extras import RealDictCursor

from transpose.common.exceptions import InstanceConnectionError
from transpose.core.sync.main import SyncClient


class DedicatedInstance:
    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        database: str = None,
        sslmode: str = None,
        debug: bool = False,
    ) -> None:
        self.debug = debug

        # connect to the database
        try:
            pool = psycopg2_pool.ThreadedConnectionPool(
                1,
                20,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                sslmode=sslmode,
            )
        except:
            raise InstanceConnectionError()

        # create a logger
        self.logger = logging.getLogger(__name__)

        # update classes
        self.__pool = pool
        self.sync = SyncClient(self)

    def _execute(self, query: str, args: tuple = ()) -> list[dict]:
        """
        Executes the given query on the dedicated instance.

        :param query: The query to execute.
        :return: The results of the query.
        """

        try:
            db = self.__pool.getconn()
            with db.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, args)
                response = cursor.fetchall()
            self.__pool.putconn(db)
            return response
        except KeyboardInterrupt:
            sys.exit()

    def fetch_schema(self, table: str) -> list[dict]:
        """
        Returns the schema for the given table.

        :param table: The table to fetch the schema for.
        :return: The schema for the given table.
        """

        row = self._execute("SELECT * FROM {} LIMIT 1;".format(table))
        return row[0].keys()
