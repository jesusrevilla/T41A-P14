import psycopg2
import pytest
from pathlib import Path

# Configura tu base de datos
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
    conn.autocommit = True
    yield conn
    conn.close()

def run_script(conn, sql_file):
    sql_path = Path(sql_file)
    with open(sql_path, "r", encoding="utf-8") as file:
        script = file.read()
    with conn.cursor() as cur:
        cur.execute(script)
        try:
            result = cur.fetchall()
        except psycopg2.ProgrammingError:
            result = []
        return result

def test_eliminar_producto(db_connection):
    # Inserta un producto para eliminarlo
    with db_connection.cursor() as cur:
        cur.execute("INSERT INTO productos(nombre, precio) VALUES ('Borrame', 99.9) RETURNING id;")
        pid = cur.fetchone()[0]
        db_connection.commit()

    result = run_script(db_connection, "01_eliminar_producto.sql")

    # Asegura que el producto fue eliminado
    with db_connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = %s;", (pid,))
        count = cur.fetchone()[0]
    assert count == 0, f"El producto con id {pid} no fue eliminado correctamente"

def test_porcentaje_precio(db_connection):
    # Crea productos de prueba
    with db_connection.cursor() as cur:
        cur.execute("DELETE FROM productos;")
        cur.execute("INSERT INTO productos(nombre, precio) VALUES ('Mouse', 100), ('Teclado', 200);")
        db_connection.commit()

    result = run_script(db_connection, "02_porcentaje_precio.sql")

    # Verifica que los precios aumentaron un 10%
    with db_connection.cursor() as cur:
        cur.execute("SELECT nombre, precio FROM productos ORDER BY nombre;")
        data = cur.fetchall()
    precios = {nombre: precio for nombre, precio in data}
    
    assert round(precios["Mouse"], 1) == 110.0
    assert round(precios["Teclado"], 1) == 220.0

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

