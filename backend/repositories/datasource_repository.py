from backend.integrations.oracle_db_client import get_connection
from backend.queries.datasource_queries import CREATE_DATASOURCE


def create_datasource(name):

    conn = get_connection()
    cursor = conn.cursor()

    datasource_id = cursor.var(int)

    cursor.execute(
        CREATE_DATASOURCE,
        {
            "name": name,
            "id": datasource_id
        }
    )

    conn.commit()

    datasource_id_value = datasource_id.getvalue()[0]

    cursor.close()
    conn.close()

    return datasource_id_value