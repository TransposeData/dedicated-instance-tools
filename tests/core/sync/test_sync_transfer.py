from transpose_dit import (
    DedicatedInstance,
    db_host,
    db_name,
    db_password,
    db_port,
    db_sslmode,
    db_username,
)
from transpose_dit.util.testing import process_single_batch


def test_sync_transfers_nominal():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    db.sync.run(process_single_batch, "ethereum.token_transfers", 1000)


def test_sync_transfers_multiple():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    assert db.sync.metadata.get("ethereum.token_transfers", {}).get("transfer", 0) == 0
    assert (
        db.sync.metadata.get("ethereum.native_token_transfers", {}).get("transfer", 0)
        == 0
    )

    db.sync.run(process_single_batch, "ethereum.token_transfers", 1000)
    db.sync.run(process_single_batch, "ethereum.native_token_transfers", 1000)

    assert db.sync.metadata.get("ethereum.token_transfers", {}).get("transfer", 0) > 0
    assert (
        db.sync.metadata.get("ethereum.native_token_transfers", {}).get("transfer", 0)
        > 0
    )


def test_sync_transfers_norows():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    # set block number to a high value to ensure no rows are returned
    db.sync.metadata["ethereum.token_transfers"] = {"transfer": 999_999_999}

    db.sync.run(process_single_batch, "ethereum.token_transfers", 1000)
