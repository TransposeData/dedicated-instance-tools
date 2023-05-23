TRANSFER_TABLE_PAGINATED_QUERY = """
    SELECT *
    FROM ethereum.token_transfers
    WHERE activity_id > %s
    ORDER BY activity_id ASC
    LIMIT %s;
"""

OWNER_TABLE_PAGINATED_QUERY = """
SELECT DISTINCT(ethereum.token_owners.*)
FROM ethereum.token_owners
JOIN LATERAL (
    SELECT from_address, to_address
    FROM ethereum.token_transfers
    WHERE activity_id > %s
    ORDER BY activity_id ASC
    LIMIT %s
) AS incremental_transfers
ON ethereum.token_owners.owner_address = incremental_transfers.from_address
OR ethereum.token_owners.owner_address = incremental_transfers.to_address;
"""
