from transpose import (
    DedicatedInstance,
    db_host,
    db_name,
    db_password,
    db_port,
    db_sslmode,
    db_username,
)
from transpose.util.testing import process_single_batch


def test_sync_owners_nominal():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    db.sync.run(process_single_batch, "ethereum.token_owners", 1000)


def test_sync_owners_multiple():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    assert db.sync.metadata.get("ethereum.token_owners", {}).get("owner", 0) == 0
    assert db.sync.metadata.get("ethereum.native_token_owners", {}).get("owner", 0) == 0

    db.sync.run(process_single_batch, "ethereum.token_owners", 1000)
    db.sync.run(process_single_batch, "ethereum.native_token_owners", 1000)

    assert db.sync.metadata.get("ethereum.token_owners", {}).get("owner", 0) > 0
    assert db.sync.metadata.get("ethereum.native_token_owners", {}).get("owner", 0) > 0
