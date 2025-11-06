import psycopg2
import pytest
from pathlib import Path
from decimal import Decimal

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
    sql_path = Path("sql") / filename  
    with open(sql_path, "r") as file:
        query = file.read()
    with conn.cursor() as cur:
        cur.execute(query)
        try:
            return cur.fetchall()
        except psycopg2.ProgrammingError:
            return []

def test_eliminar_producto(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 1;")
        assert cur.fetchone()[0] == 1

        cur.execute("CALL eliminar_producto(1);")

        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 1;")
        assert cur.fetchone()[0] == 0


def test_aumentar_precios(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT precio FROM productos WHERE nombre = 'Mouse';")
        precio_original = cur.fetchone()[0]

        cur.execute("CALL aumentar_precios(10);")

        cur.execute("SELECT precio FROM productos WHERE nombre = 'Mouse';")
        precio_nuevo = cur.fetchone()[0]

        assert round(precio_nuevo, 2) == round(precio_original * Decimal('1.10'), 2)


def test_productos_por_rango(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT id, nombre, precio FROM productos
            WHERE precio BETWEEN 50 AND 200 ORDER BY precio;
        """)
        resultados = cur.fetchall()
        nombres = [r[1] for r in resultados]

        assert "Mouse" in nombres
        assert "Auriculares" in nombres
        assert "Teclado" in nombres



