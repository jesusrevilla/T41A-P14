import psycopg2
import pytest
from pathlib import Path

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    yield conn
    conn.close()

def run_query_from_file(conn, filename):
    sql_path = Path(filename)
    with open(sql_path, "r") as file:
        query = file.read()
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def test_elimina_por_id(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 1;")
        assert cur.fetchone()[0] == 1
        cur.execute("CALL eliminar_producto(1);")
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 1;")
        assert cur.fetchone()[0] == 0
    



