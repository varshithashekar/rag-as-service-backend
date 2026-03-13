INSERT_FILE = """
INSERT INTO RAG_SERVICE_FILE_STATUS
(
    DATASOURCE_ID,
    FILE_NAME,
    FILE_PATH,
    FILE_TYPE,
    FILE_SIZE_BYTES,
    STATUS,
    RETRIES,
    CREATED_AT,
    UPDATED_AT
)
VALUES
(
    :datasource_id,
    :file_name,
    :file_path,
    :file_type,
    :file_size,
    'PENDING',
    0,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
"""