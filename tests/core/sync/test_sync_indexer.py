from copy import deepcopy

from transpose_dit import (
    DedicatedInstance,
    db_host,
    db_name,
    db_password,
    db_port,
    db_sslmode,
    db_username,
)
from transpose_dit.util.testing import (
    MULTI_SYNC_METADATA,
    NFT_SALES_METADATA,
    process_single_batch,
)


def test_sync_indexer_nominal():
    db = DedicatedInstance(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_name,
        sslmode=db_sslmode,
    )
    assert isinstance(db, (DedicatedInstance,))

    # grab initial metadata to avoid long fetch
    db.sync.metadata = deepcopy(NFT_SALES_METADATA)

    db.sync.run(process_single_batch, "ethereum.nft_sales", 1000)


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

    # grab initial metadata to avoid long fetch
    db.sync.metadata = deepcopy(MULTI_SYNC_METADATA)

    nft_sale_values = (
        db.sync.metadata.get("ethereum.nft_sales", {}).get("indexer_ids", {}).values()
    )
    token_price_values = (
        db.sync.metadata.get("ethereum.token_prices", {})
        .get("indexer_ids", {})
        .values()
    )
    assert all(value == 0 for value in nft_sale_values)
    assert all(value == 0 for value in token_price_values)

    db.sync.run(process_single_batch, "ethereum.nft_sales", 1000)
    db.sync.run(process_single_batch, "ethereum.token_prices", 1000)

    # assert any indexer progress was made
    nft_sale_values = (
        db.sync.metadata.get("ethereum.nft_sales", {}).get("indexer_ids", {}).values()
    )
    token_price_values = (
        db.sync.metadata.get("ethereum.token_prices", {})
        .get("indexer_ids", {})
        .values()
    )
    assert any(value > 0 for value in nft_sale_values)
    assert any(value > 0 for value in token_price_values)
