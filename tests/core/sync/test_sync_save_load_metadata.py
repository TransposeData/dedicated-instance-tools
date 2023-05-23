import os

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


def test_sync_save_metadata():
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
    db.sync.save_metadata()

    # assert metadata.json exists
    assert os.path.exists("metadata.json")
    os.remove("metadata.json")


def test_sync_load_metadata():
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
    db.sync.save_metadata()

    # assert metadata.json exists
    assert os.path.exists("metadata.json")

    db2 = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db2, (DedicatedInstance,))
    db2.sync.load_metadata()

    os.remove("metadata.json")

    # assert the metadatas match
    assert db.sync.metadata == db2.sync.metadata
