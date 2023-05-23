TRANSFER_TABLE_PAGINATED_QUERY = """
    SELECT *
    FROM {}
    WHERE activity_id > %s
    ORDER BY activity_id ASC
    LIMIT %s;
"""

OWNER_TABLE_PAGINATED_QUERY = """
SELECT *
FROM {} AS owners
WHERE owner_address = ANY(%s)
"""

INDEXER_TABLE_PAGINATED_QUERY = """
SELECT *
FROM {}
WHERE (__indexer_id = %s AND __block_number >= %s)
ORDER BY __indexer_id, __block_number ASC
LIMIT %s;
"""
