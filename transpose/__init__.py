import os

from dotenv import load_dotenv

load_dotenv()

db_host = os.environ.get("HOST")
db_port = os.environ.get("PORT")
db_username = os.environ.get("USERNAME")
db_password = os.environ.get("PASSWORD")
db_name = os.environ.get("DATABASE")
db_sslmode = os.environ.get("SSLMODE")

# this file is important for nice imports
from transpose.core.main import DedicatedInstance  # noqa
