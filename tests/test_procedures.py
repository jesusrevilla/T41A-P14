import pytest
import psycopg2
import os
from pytest import approx # Para comparar números decimales



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



def test_eliminar_producto_exitoso(db_cursor):
    """Prueba que el procedure elimina correctamente un producto existente."""


    db_cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
        ('Producto para Borrar', 99.99)
    )
    producto_id_prueba = db_cursor.fetchone()[0]


    db_cursor.execute("CALL eliminar_producto(%s);", (producto_id_prueba,))


    db_cursor.execute("SELECT COUNT(*) FROM productos WHERE id = %s;", (producto_id_prueba,))
    count = db_cursor.fetchone()[0]

    assert count == 0, f"El producto con ID {producto_id_prueba} no fue eliminado."


def test_eliminar_producto_no_existente(db_cursor):
    """Prueba que el procedure no falle si intenta borrar un ID que no existe."""

    id_inexistente = -1 

    try:
    
        db_cursor.execute("CALL eliminar_producto(%s);", (id_inexistente,))


      
        assert True

    except Exception as e:
        pytest.fail(f"El procedure falló al intentar borrar un ID inexistente: {e}")




def test_actualizar_precio_producto(db_cursor):
    """
    Prueba que el procedure actualiza el precio de un producto 
    basado en un porcentaje.
    """


    db_cursor.execute(
        "INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
        ('Producto para Actualizar', 100.00)
    )
    producto_id_prueba = db_cursor.fetchone()[0]


  
    porcentaje_aumento = 10 
    db_cursor.execute("CALL actualizar_precio_por_porcentaje(%s);", (porcentaje_aumento,))


  
    db_cursor.execute("SELECT precio FROM productos WHERE id = %s;", (producto_id_prueba,))

   
    nuevo_precio = db_cursor.fetchone()[0] 

  
    assert nuevo_precio == approx(110.00)



def test_sp_mostrar_productos_por_rango_no_falla(db_cursor):

    db_cursor.execute(
        """
        INSERT INTO productos (nombre, precio) VALUES
        ('Test Rango A', 10.00),
        ('Test Rango B', 50.00);
        """
    )

    try:
       
        db_cursor.execute("CALL sp_mostrar_productos_por_rango(%s, %s);", (40.00, 60.00))

        
        assert True

    except Exception as e:
        pytest.fail(f"El procedure 'sp_mostrar_productos_por_rango' falló al ejecutarse: {e}")
