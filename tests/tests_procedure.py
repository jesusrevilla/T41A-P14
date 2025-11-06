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
    result = run_query_from_file(db_connection, "03_elimina_por_id.sql")
    names = [row[0] for row in result]
    mensaje_exito_esperado = 'Se elimino el producto exitosamente.\n' 
    mensaje_no_encontrado_esperado = 'No se encontro el producto\n'
    assert any(str(notice) == mensaje_exito_esperado for notice in notices_exito), \
        f"No se encontró el notice de éxito esperado: '{mensaje_exito_esperado}'"
    assert any(str(notice) == mensaje_no_encontrado_esperado for notice in notices_no_encontrado), \
        f"No se encontró el notice de no encontrado esperado: '{mensaje_no_encontrado_esperado}'"




def test_porcentaje(db_connection):
    result = run_query_from_file(db_connection, "04_porcentaje_producto.sql")
    names = [row[0] for row in result]
    assert set(names) == {"Ana", "Luis", "Carlos"}


