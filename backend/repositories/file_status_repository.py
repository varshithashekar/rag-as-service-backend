from backend.integrations.oracle_db_client import get_connection
from backend.queries.file_status_queries import INSERT_FILE


def insert_file_record(
    datasource_id,
    file_name,
    file_path,
    file_type,
    file_size
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        INSERT_FILE,
        {
            "datasource_id": datasource_id,
            "file_name": file_name,
            "file_path": file_path,
            "file_type": file_type,
            "file_size": file_size
        }
    )

    conn.commit()

    cursor.close()
    conn.close()