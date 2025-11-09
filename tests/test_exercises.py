import pytest
import psycopg2
from pytest import approx

# --- Configuración de la base de datos ---
DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

# --- Fixture de conexión con rollback ---
@pytest.fixture(scope="function")
def db_cursor():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        cursor = conn.cursor()
        yield cursor
    except Exception as e:
        pytest.fail(f"No se pudo conectar a la base de datos: {e}")
    finally:
        if conn:
            print("\n[ROLLBACK] Revirtiendo cambios de la prueba...")
            conn.rollback()
            if cursor:
                cursor.close()
            conn.close()

# --- Prueba del procedure 'eliminar_id' ---
def test_eliminar_id_exitoso(db_cursor):
    db_cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
        ('Producto para Borrar', 99.99)
    )
    producto_id = db_cursor.fetchone()[0]

    db_cursor.execute("CALL eliminar_id(%s);", (producto_id,))

    db_cursor.execute("SELECT COUNT(*) FROM productos WHERE id = %s;", (producto_id,))
    count = db_cursor.fetchone()[0]

    assert count == 0, f"El producto con ID {producto_id} no fue eliminado."


def test_eliminar_id_inexistente(db_cursor):
    id_inexistente = -1
    try:
        db_cursor.execute("CALL eliminar_id(%s);", (id_inexistente,))
        assert True
    except Exception as e:
        pytest.fail(f"El procedure 'eliminar_id' falló al intentar borrar un ID inexistente: {e}")

# --- Prueba del procedure 'aumenta_precio' ---
def test_aumenta_precio(db_cursor):
    db_cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
        ('Producto para Aumentar', 100.00)
    )
    producto_id = db_cursor.fetchone()[0]

    porcentaje = 10  # Aumentar 10%
    db_cursor.execute("CALL aumenta_precio(%s);", (porcentaje,))

    db_cursor.execute("SELECT precio FROM productos WHERE id = %s;", (producto_id,))
    nuevo_precio = db_cursor.fetchone()[0]

    assert nuevo_precio == approx(110.00)

# --- Prueba del function 'busqueda_por_rango' ---
def test_busqueda_por_rango_funciona(db_cursor):
    db_cursor.execute("""
        INSERT INTO productos (nombre, precio) VALUES
        ('Producto Rango A', 10.00),
        ('Producto Rango B', 50.00),
        ('Producto Rango C', 500.00);
    """)

    db_cursor.execute("SELECT * FROM busqueda_por_rango(%s, %s);", (0, 100))
    resultados = db_cursor.fetchall()

    # Debe devolver los productos dentro del rango 0–100
    assert len(resultados) == 2, "La función no devolvió los productos esperados."

