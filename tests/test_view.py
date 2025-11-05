import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",    
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="module")
def db_connection():
    """Conexión a la base de datos"""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def reset_data(db_connection):
    """Reinicia los datos antes de cada test"""
    with db_connection.cursor() as cur:
        cur.execute("DELETE FROM auditoria_productos;")
        cur.execute("DELETE FROM productos;")
        cur.execute("""
            INSERT INTO productos (nombre, precio) VALUES
            ('Teclado', 100.00),
            ('Mouse', 50.00),
            ('Monitor', 600.00),
            ('Laptop', 1500.00),
            ('Auriculares', 80.00);
        """)
    yield

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

        assert round(precio_nuevo, 2) == round(precio_original * 1.10, 2)


def test_productos_por_rango(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT id, nombre, precio FROM productos
            WHERE precio BETWEEN 50 AND 150 ORDER BY precio;
        """)
        resultados = cur.fetchall()
        nombres = [r[1] for r in resultados]

        assert "Mouse" in nombres
        assert "Auriculares" in nombres
        assert "Teclado" in nombres
        assert "Laptop" not in nombres


def test_actualizar_precio_auditado(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT precio FROM productos WHERE id = 2;")
        precio_anterior = cur.fetchone()[0]

        cur.execute("CALL actualizar_precio_auditado(2, 120.00);")

        cur.execute("SELECT precio FROM productos WHERE id = 2;")
        precio_nuevo = cur.fetchone()[0]
        assert round(precio_nuevo, 2) == 120.00

        cur.execute("SELECT accion FROM auditoria_productos WHERE producto_id = 2;")
        auditoria = cur.fetchone()
        assert auditoria is not None
        assert "Actualización" in auditoria[0]
