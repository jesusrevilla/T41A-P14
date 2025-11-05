import psycopg2
import pytest
from decimal import Decimal

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture
def db_connection():
    notices = []
    
    def notice_receiver(notice):
        notices.append(notice.diag.message_primary)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.add_notice_receiver(notice_receiver)
    
    yield conn, notices
    
    conn.rollback()
    conn.close()


def test_eliminar_producto_existente(db_connection):
    conn, notices = db_connection
    product_id_to_delete = 3

    with conn.cursor() as cur:
        cur.execute("CALL eliminar_producto(%s);", (product_id_to_delete,))
        
        cur.execute("SELECT * FROM productos WHERE id = %s;", (product_id_to_delete,))
        result = cur.fetchone()
        assert result is None

    conn.commit()
    assert any("Producto eliminado exitosamente" in n for n in notices)


def test_eliminar_producto_no_existente(db_connection):
    conn, notices = db_connection
    product_id_to_delete = 9999

    with conn.cursor() as cur:
        cur.execute("CALL eliminar_producto(%s);", (product_id_to_delete,))
        
        cur.execute("SELECT * FROM productos WHERE id = %s;", (product_id_to_delete,))
        result = cur.fetchone()
        assert result is None

    conn.commit()
    assert any("No se encontró un producto" in n for n in notices)


def test_aumentar_precios(db_connection):
    conn, notices = db_connection
    aumento = Decimal('10.00')
    
    with conn.cursor() as cur:
        cur.execute("SELECT precio FROM productos WHERE id = 1;")
        precio_original = cur.fetchone()[0]
    
    precio_esperado = precio_original * (Decimal('1') + (aumento / Decimal('100')))

    with conn.cursor() as cur:
        cur.execute("CALL aumentar_precios(%s);", (aumento,))

    with conn.cursor() as cur:
        cur.execute("SELECT precio FROM productos WHERE id = 1;")
        nuevo_precio = cur.fetchone()[0]
        
        assert nuevo_precio == precio_esperado

    conn.commit()
    assert any("Precios actualizados. 5 filas afectadas." in n for n in notices)


def test_buscar_por_rango(db_connection):
    conn, notices = db_connection
    
    with conn.cursor() as cur:
        cur.execute("CALL buscar_por_rango(50.00, 150.00);")

    conn.commit() 

    log_completo = "\n".join(notices)
    
    assert "--- Productos encontrados (Rango: 50.00 a 150.00) ---" in log_completo
    assert "Nombre: Audífonos Inalámbricos" in log_completo
    assert "Nombre: Teclado Mecánico RGB" in log_completo
    assert "Nombre: Laptop Gamer X1" not in log_completo
    assert "Fin de la búsqueda" in log_completo
