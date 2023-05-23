NFT_SALES_METADATA = {
    "ethereum.nft_sales": {
        "indexer_ids": {
            "zero-x-v0-nft-sales": 0,
            "opensea-seaport-nft-sales-v0": 0,
            "opensea-wyvern-nft-sales": 0,
        },
        "batches_till_sync": 100,
    }
}

MULTI_SYNC_METADATA = {
    "ethereum.nft_sales": {
        "indexer_ids": {
            "zero-x-v0-nft-sales": 0,
            "opensea-seaport-nft-sales-v0": 0,
            "opensea-wyvern-nft-sales": 0,
        },
        "batches_till_sync": 100,
    },
    "ethereum.token_prices": {
        "indexer_ids": {
            "aave-token-prices": 0,
            "balancer-v2-lp-token-prices": 0,
            "balancer-v1-lp-token-prices": 0,
        },
        "batches_till_sync": 100,
    },
}


def process_single_batch(rows: list[dict]) -> None:
    assert isinstance(rows, (list,))
    assert isinstance(rows[0], (dict,))
    assert len(rows) > 0
    return False
