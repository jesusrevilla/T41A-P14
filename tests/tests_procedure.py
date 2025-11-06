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
    results, notices_list = run_query_from_file(db_connection, "03_elimina_por_id.sql")
    mensaje_exito_esperado = 'NOTICE: Se elimino el producto exitosamente.\n' 
    mensaje_no_encontrado_esperado = 'NOTICE: No se encontro el producto\n'
    assert any(mensaje_exito_esperado == notice for notice in notices_list), \
        f"Falta el NOTICE de éxito esperado. Notices capturados: {notices_list}"
    assert any(mensaje_no_encontrado_esperado == notice for notice in notices_list), \
        f"Falta el NOTICE de no encontrado esperado. Notices capturados: {notices_list}"
    



