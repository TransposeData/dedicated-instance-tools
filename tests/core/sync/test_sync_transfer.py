from transpose import (
    DedicatedInstance,
    db_host,
    db_name,
    db_password,
    db_port,
    db_sslmode,
    db_username,
)


def test_sync_transfers():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    db.sync.run(print, "ethereum.token_transfers", 1000)
