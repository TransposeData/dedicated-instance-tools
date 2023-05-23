from transpose_dit import (
    DedicatedInstance,
    db_host,
    db_name,
    db_password,
    db_port,
    db_sslmode,
    db_username,
)


def test_sync_classification_transfers():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    assert db.sync._classify_table("ethereum.native_token_transfers") == "transfer"
    assert db.sync._classify_table("ethereum.token_transfers") == "transfer"


def test_sync_classification_indexers():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    assert db.sync._classify_table("ethereum.token_prices") == "indexer"
    assert db.sync._classify_table("ethereum.nft_sales") == "indexer"


def test_sync_classification_owners():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    assert db.sync._classify_table("ethereum.native_token_owners") == "owner"
    assert db.sync._classify_table("ethereum.token_owners") == "owner"


def test_sync_invalid():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    try:
        db.sync._classify_table("ethereum.traces")
        assert False
    except:
        assert True
