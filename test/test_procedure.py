import psycopg2
from decimal import Decimal

def test_eliminar_producto():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("CALL eliminar_producto(3);")
    
    assert len(conn.notices) == 1
    assert "Producto eliminado" in conn.notices[0]

    cur.execute("SELECT COUNT(*) FROM productos WHERE id = 3;")
    count = cur.fetchone()[0]
    assert count == 0

def test_eliminar_producto_no_encontrado():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    cur.execute("CALL eliminar_producto(999);")

    assert len(conn.notices) == 1
    assert "Producto no encontrado" in conn.notices[0]


def test_aumentar_precios():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
  
    cur.execute("CALL aumentar_precios(10.0);")
    cur.execute("SELECT precio FROM productos WHERE id = 2;")

    precio_monitor = cur.fetchone()[0]
    assert precio_monitor == Decimal('274.45')

    cur.execute("SELECT precio FROM productos WHERE id = 10;")
    precio_mochila = cur.fetchone()[0]
    assert precio_mochila == Decimal('49.72')

def test_buscar_por_rango():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    cur.execute("CALL buscar_por_rango(50.00, 100.00);")
    cur.execute("SELECT nombre FROM tmp_resultados_productos ORDER BY nombre;")
    
    resultados = cur.fetchall()
    nombres = [row[0] for row in resultados]
    
    assert len(nombres) == 3
    assert "Teclado Mecánico Keychron" in nombres
    assert "Mouse Logitech MX Master 3" in nombres
    assert "Disco Duro Externo 1TB" in nombres

def test_actualizar_producto_y_auditoria():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    nuevo_nombre = "Mouse Logitech Pro"
    nuevo_precio = Decimal('115.50')
    
    cur.execute("CALL actualizar_producto(4, %s, %s);", (nuevo_nombre, nuevo_precio))

    cur.execute("SELECT nombre, precio FROM productos WHERE id = 4;")
    producto = cur.fetchone()
    assert producto[0] == nuevo_nombre
    assert producto[1] == nuevo_precio

    cur.execute("SELECT * FROM productos_auditoria;")
    logs = cur.fetchall()
    
    assert len(logs) == 1
    
    log = logs[0]

    assert log[1] == 4 
    assert log[2] == 'Mouse Logitech MX Master 3'
    assert log[3] == Decimal('99.90')
    assert log[4] == nuevo_nombre
    assert log[5] == nuevo_precio 
