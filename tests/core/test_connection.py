from transpose_dit import (
    DedicatedInstance,
    db_host,
    db_name,
    db_password,
    db_port,
    db_sslmode,
    db_username,
)


def test_valid_connection():
    try:
        db = DedicatedInstance(
            host=db_host,
            port=db_port,
            user=db_username,
            password=db_password,
            database=db_name,
            sslmode=db_sslmode,
        )
        assert isinstance(db, (DedicatedInstance,))
    except Exception:
        assert False


def test_invalid_connection():
    try:
        DedicatedInstance()
        assert False
    except Exception:
        assert True
