import os

from dotenv import load_dotenv

from transpose.core.main import DedicatedInstance

load_dotenv()

db = DedicatedInstance(
    host=os.environ.get("HOST"),
    port=os.environ.get("PORT"),
    user=os.environ.get("USERNAME"),
    password=os.environ.get("PASSWORD"),
    database=os.environ.get("DATABASE"),
    sslmode=os.environ.get("SSLMODE"),
    debug=False,
)


def proccess_rows(rows: list[dict]) -> None:
    # just print the rows
    # print(rows)
    pass


db.sync.run(proccess_rows, "ethereum.native_token_transfers", 10_000)
