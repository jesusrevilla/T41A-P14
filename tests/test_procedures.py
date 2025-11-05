import pytest
import psycopg2
import os
from pytest import approx # Para comparar números decimales


# --- Fixture de Base de Datos (con Rollback) ---
# Esta es la parte clave para probar procedimientos de escritura
DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="function")
def db_cursor():
    """
    Fixture de Pytest para manejar la conexión y las transacciones de la BD.
    
    - scope="function" significa que esto se ejecuta CADA VEZ por CADA prueba.
    - Se conecta a la BD antes de cada prueba.
    - Crea un cursor DENTRO de una transacción.
    - Entrega (yield) el cursor a la prueba.
    - Hace ROLLBACK después de que la prueba termina.
    """
    conn = None
    cursor = None
    try:
        # Leemos las credenciales del .env (gracias a load_dotenv)
        conn = psycopg2.connect(**DB_CONFIG)
        
        # Desactivamos autocommit para controlar la transacción
        conn.autocommit = False 
        cursor = conn.cursor()

        # "yield" entrega el control a la función de prueba
        yield cursor

    except Exception as e:
        pytest.fail(f"No se pudo conectar a la base de datos: {e}")
    
    finally:
        # Esto se ejecuta DESPUÉS de cada prueba
        if conn:
            print("\n[ROLLBACK] Revirtiendo cambios de la prueba...")
            conn.rollback() # ¡La parte más importante!
            if cursor:
                cursor.close()
            conn.close()

# --- Pruebas del Procedure 'eliminar_producto' ---

def test_eliminar_producto_exitoso(db_cursor):
    """Prueba que el procedure elimina correctamente un producto existente."""
    
    # 1. ARRANGE
    db_cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
        ('Producto para Borrar', 99.99)
    )
    producto_id_prueba = db_cursor.fetchone()[0]

    # 2. ACT
    db_cursor.execute("CALL eliminar_producto(%s);", (producto_id_prueba,))

    # 3. ASSERT
    db_cursor.execute("SELECT COUNT(*) FROM productos WHERE id = %s;", (producto_id_prueba,))
    count = db_cursor.fetchone()[0]
    
    assert count == 0, f"El producto con ID {producto_id_prueba} no fue eliminado."


def test_eliminar_producto_no_existente(db_cursor):
    """Prueba que el procedure no falle si intenta borrar un ID que no existe."""
    
    id_inexistente = -1 
    
    try:
        # 2. ACT
        db_cursor.execute("CALL eliminar_producto(%s);", (id_inexistente,))
        
        # 3. ASSERT
        # La prueba pasa si la línea anterior no lanzó una excepción
        assert True
        
    except Exception as e:
        pytest.fail(f"El procedure falló al intentar borrar un ID inexistente: {e}")


# --- Pruebas del Procedure 'actualizar_precio_producto' ---

def test_actualizar_precio_producto(db_cursor):
    """
    Prueba que el procedure actualiza el precio de un producto 
    basado en un porcentaje.
    """
    
    # 1. ARRANGE
    # Insertamos un producto con un precio conocido (ej. 100.00)
    db_cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
        ('Producto para Actualizar', 100.00)
    )
    producto_id_prueba = db_cursor.fetchone()[0]
    
    # 2. ACT
    # Llamamos al procedure para aumentar el precio en 10% (0.10)
    # Tu procedure suma 1 + 0.10
    porcentaje_aumento = 0.10 
    db_cursor.execute("CALL actualizar_precio_producto(%s, %s);", (producto_id_prueba, porcentaje_aumento))

    # 3. ASSERT
    # Verificamos que el nuevo precio sea 110.00
    db_cursor.execute("SELECT precio FROM productos WHERE id = %s;", (producto_id_prueba,))
    
    # fetchone() devuelve una tupla, ej. (Decimal('110.00'),)
    nuevo_precio = db_cursor.fetchone()[0] 
    
    # Usamos pytest.approx para manejar la comparación de números decimales (floats)
    # 100.00 * (1 + 0.10) = 110.00
    assert nuevo_precio == approx(110.00)

# --- Prueba para 'sp_mostrar_productos_por_rango' (El que usa RAISE NOTICE) ---

def test_sp_mostrar_productos_por_rango_no_falla(db_cursor):
    # 1. ARRANGE
    db_cursor.execute(
        """
        INSERT INTO productos (nombre, precio) VALUES
        ('Test Rango A', 10.00),
        ('Test Rango B', 50.00);
        """
    )
    
    try:
        # 2. ACT
        # Llamamos al procedure
        db_cursor.execute("CALL sp_mostrar_productos_por_rango(%s, %s);", (40.00, 60.00))
        
        # 3. ASSERT
        # Si llegamos aquí sin un error de psycopg2, el procedure "funcionó"
        assert True
        
    except Exception as e:
        pytest.fail(f"El procedure 'sp_mostrar_productos_por_rango' falló al ejecutarse: {e}")
