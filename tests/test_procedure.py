import psycopg2
import pytest
from pathlib import Path

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
    sql_path = Path(filename)
    with open(sql_path, "r") as file:
        query = file.read()
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def test_elimina_por_id(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 2;")
        assert cur.fetchone()[0] == 1
        cur.execute("CALL eliminar_producto(2);")
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = 2;")
        assert cur.fetchone()[0] == 0

def test_rango(db_connection):
    precio_min = 10
    precio_max = 400
    productos_esperados = ['Teclado'] 
    with db_connection.cursor() as cur:
        sql_call = f"""
        DO $$
        DECLARE
            out_lista TEXT;
        BEGIN
            -- Los valores se insertan como constantes en la cadena SQL.
            -- Usamos {precio_min} y {precio_max}
            CALL rango_precio({precio_min}, {precio_max}, out_lista); 
            
            EXECUTE format('SET session rangos.lista_productos = %L', out_lista);
        END
        $$;
        """
        cur.execute(sql_call)
        cur.execute("SHOW rangos.lista_productos;")
        resultado = cur.fetchone()[0]
        for producto in productos_esperados:
            assert producto in resultado


    
def test_porcentaje(db_connection):
    PRODUCTO_NOMBRE = 'Teclado'
    PRECIO_INICIAL = 299.99
    PORCENTAJE = 10.00
    PRECIO_ESPERADO = 329.99 
    with db_connection.cursor() as cur:
        cur.execute(
            "UPDATE productos SET precio = %s WHERE nombre = %s;",
            (PRECIO_INICIAL, PRODUCTO_NOMBRE)
        )
        db_connection.commit()
        cur.execute("CALL porcentaje_producto(%s);", (PORCENTAJE,))
        db_connection.commit()
        cur.execute(
            "SELECT ROUND(precio, 2) FROM productos WHERE nombre = %s;",
            (PRODUCTO_NOMBRE,)
        )
        precio_actualizado_db = cur.fetchone()[0]
        assert float(precio_actualizado_db) == pytest.approx(PRECIO_ESPERADO)


