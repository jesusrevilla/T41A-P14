import psycopg2
import pytest
from pathlib import Path

# Configuración de la base de datos
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
    """
    Ejecuta el contenido de un archivo SQL y devuelve los resultados (si existen).
    """
    sql_path = Path(filename)
    with open(sql_path, "r") as file:
        query = file.read()
    with conn.cursor() as cur:
        cur.execute(query)
        try:
            return cur.fetchall()
        except psycopg2.ProgrammingError:
            # No hay resultados (por ejemplo en un procedimiento sin SELECT)
            conn.commit()
            return []

# ----------------------------------------------------------------------
# TEST 1 - Eliminar producto
# ----------------------------------------------------------------------

def test_eliminar_producto(db_connection):
    """
    Verifica que el procedimiento eliminar_producto elimina correctamente un producto existente.
    """
    conn = db_connection
    # Inserta producto de prueba
    with conn.cursor() as cur:
        cur.execute("INSERT INTO productos (nombre, precio) VALUES ('Borrame', 100);")
        conn.commit()
    
    # Ejecuta el procedimiento
    run_query_from_file(conn, "PROCEDURE_1.sql")

    # Verifica que ya no exista
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos WHERE nombre='Borrame';")
        count = cur.fetchone()[0]
    assert count == 0

# ----------------------------------------------------------------------
# TEST 2 - Aumentar precios
# ----------------------------------------------------------------------

def test_aumentar_precios(db_connection):
    """
    Verifica que el procedimiento aumentar_precios aumenta correctamente los precios.
    """
    conn = db_connection
    with conn.cursor() as cur:
        cur.execute("SELECT AVG(precio) FROM productos;")
        precio_inicial = cur.fetchone()[0]

    run_query_from_file(conn, "PROCEDURE_2.sql")

    with conn.cursor() as cur:
        cur.execute("SELECT AVG(precio) FROM productos;")
        precio_final = cur.fetchone()[0]

    assert precio_final > precio_inicial

# ----------------------------------------------------------------------
# TEST 3 - Productos en rango de precios
# ----------------------------------------------------------------------
'''
def test_productos_en_rango(db_connection):
    """
    Verifica que el procedimiento devuelve productos dentro del rango especificado.
    """
    result = run_query_from_file(db_connection, "03_productos_en_rango.sql")
    assert len(result) > 0
    for row in result:
        assert 100 <= row[1] <= 1000  # Suponiendo que el rango es 100 a 1000
'''
# ----------------------------------------------------------------------
# TEST 4 - Auditoría
# ----------------------------------------------------------------------
'''
def test_registrar_auditoria(db_connection):
    """
    Verifica que se inserta un registro en la tabla de auditoría al actualizar un producto.
    """
    conn = db_connection
    run_query_from_file(conn, "04_registrar_auditoria.sql")

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM auditoria;")
        count = cur.fetchone()[0]
    assert count > 0'''

