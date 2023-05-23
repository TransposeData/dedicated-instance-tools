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


def test_sync_fetch_indexers():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    db.sync.run(process_single_batch, "ethereum.ens_names", 1000)

    assert (
        "ens-addr-changed"
        in db.sync.metadata.get("ethereum.ens_names", {}).get("indexer_ids", {}).keys()
    )
    assert (
        "ens-name-registered"
        in db.sync.metadata.get("ethereum.ens_names", {}).get("indexer_ids", {}).keys()
    )
    assert (
        "ens-name-renewed"
        in db.sync.metadata.get("ethereum.ens_names", {}).get("indexer_ids", {}).keys()
    )
    assert (
        "ens-new-resolver"
        in db.sync.metadata.get("ethereum.ens_names", {}).get("indexer_ids", {}).keys()
    )
    assert (
        "ens-reverse-registrar"
        in db.sync.metadata.get("ethereum.ens_names", {}).get("indexer_ids", {}).keys()
    )
    assert (
        "ens-transfer"
        in db.sync.metadata.get("ethereum.ens_names", {}).get("indexer_ids", {}).keys()
    )
