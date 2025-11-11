import psycopg2
import pytest

# Configuración de la conexión
DB_HOST = "localhost"
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Conectar a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# 1. Test para verificar la inserción de productos
def test_insertar_productos():
    conn = get_db_connection()
    cur = conn.cursor()

    # Insertar un nuevo producto
    cur.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                ('Tablet', 1000.00, 20))
    conn.commit()

    # Verificar que el producto fue insertado
    cur.execute("SELECT nombre FROM productos WHERE nombre = 'Tablet'")
    result = cur.fetchone()
    assert result is not None
    assert result[0] == 'Tablet'

    cur.close()
    conn.close()

# 2. Test para eliminar un producto
def test_eliminar_producto():
    conn = get_db_connection()
    cur = conn.cursor()

    # Eliminar un producto por ID (usamos el ID de la 'Tablet' insertada)
    cur.execute("DELETE FROM productos WHERE nombre = 'Tablet'")
    conn.commit()

    # Verificar que el producto ha sido eliminado
    cur.execute("SELECT nombre FROM productos WHERE nombre = 'Tablet'")
    result = cur.fetchone()
    assert result is None

    cur.close()
    conn.close()

# 3. Test para aumentar los precios
def test_aumentar_precios():
    conn = get_db_connection()
    cur = conn.cursor()

    # Aumentar los precios en un 10%
    cur.execute("CALL aumentar_precios(10)")
    conn.commit()

    # Verificar que el precio de un producto específico aumentó
    cur.execute("SELECT precio FROM productos WHERE nombre = 'Laptop'")
    result = cur.fetchone()
    assert result is not None
    assert result[0] == 15000.00 * 1.10  # 10% más que el precio original

    cur.close()
    conn.close()

# 4. Test para obtener productos en un rango de precios
def test_obtener_productos_rango():
    conn = get_db_connection()
    cur = conn.cursor()

    # Obtener productos en el rango de precios entre 100 y 1000
    cur.execute("SELECT * FROM obtener_productos_rango(100, 1000)")
    result = cur.fetchall()

    # Verificar que los productos devueltos estén en el rango esperado
    for row in result:
        assert 100 <= row[2] <= 1000  # Verificar que el precio esté en el rango

    cur.close()
    conn.close()
