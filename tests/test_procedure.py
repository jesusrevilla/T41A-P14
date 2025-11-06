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
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 2;")
        assert cur.fetchone()[0] == 1
        cur.execute("CALL eliminar_producto(2);")
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 2;")
        assert cur.fetchone()[0] == 0

def test_rango(db_connection):
    productos_esperados = ['Teclado'] 
    with db_connection.cursor() as cur:
        sql_call = """
        DO $$
        DECLARE 
            out_lista TEXT;
        BEGIN
            CALL rango_precio(%s, %s, out_lista); 
            EXECUTE format('SET session rangos.lista_productos = %L', out_lista);
        END
        $$;
        """
        cur.execute(sql_call, (10, 400))
        cur.execute("SHOW rangos.lista_productos;")
        resultado = cur.fetchone()[0]
        for producto in productos_esperados:
            assert producto in resultado


    



