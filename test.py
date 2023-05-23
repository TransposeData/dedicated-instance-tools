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
    debug=True,
)

db.sync.run(print, "ethereum.nft_sales", 1000)
