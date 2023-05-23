import os

from dotenv import load_dotenv

from transpose import DedicatedInstance

load_dotenv()
db = DedicatedInstance(
    host=os.environ.get("HOST"),
    port=os.environ.get("PORT"),
    user=os.environ.get("USERNAME"),
    password=os.environ.get("PASSWORD"),
    database=os.environ.get("DATABASE"),
    sslmode=os.environ.get("SSLMODE"),
    debug=True,
)


def proccess_rows(rows: list[dict]) -> None:

    # do something with the rows
    # ...
    for row in rows:
        print(row)

    # you can return False to stop the sync
    return True


try:
    # load the sync progress
    db.sync.load_metadata("metadata.json")

    # run the sync
    db.sync.run(proccess_rows, "ethereum.nft_sales", 1_000)
except KeyboardInterrupt:

    # save the sync progress if the sync was interrupted
    db.sync.save_metadata("metadata.json")
