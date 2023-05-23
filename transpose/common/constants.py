TRANSFER_TABLE_PAGINATED_QUERY = """
    SELECT *
    FROM {}
    WHERE activity_id > %s
    ORDER BY activity_id ASC
    LIMIT %s;
"""

OWNER_TABLE_PAGINATED_QUERY = """
SELECT DISTINCT(owners.*), transfers.activity_id
FROM {} AS owners
JOIN (
    SELECT from_address, to_address, activity_id
    FROM {}
    WHERE activity_id > %s
    ORDER BY activity_id ASC
    LIMIT %s
) AS transfers
ON owners.owner_address = transfers.from_address
OR owners.owner_address = transfers.to_address;

"""

INDEXER_TABLE_PAGINATED_QUERY = """
SELECT *
FROM {}
WHERE (__indexer_id = %s AND __block_number >= %s)
ORDER BY __indexer_id, __block_number ASC
LIMIT %s;
"""
