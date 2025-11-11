
import psycopg2
import pytest
from decimal import Decimal

def test_database_procedures_execution():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname='test_db',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        cur = conn.cursor()

        cur.execute("SELECT * FROM productos WHERE id = 1;")
        producto_eliminado = cur.fetchone()
        assert producto_eliminado is None, "El producto con ID 1 (Laptop) no fue eliminado."

        cur.execute("SELECT COUNT(*) FROM productos;")
        conteo_total = cur.fetchone()[0]
        assert conteo_total == 11, f"Se esperaban 11 productos, pero se encontraron {conteo_total}."

        cur.execute("SELECT precio FROM productos WHERE id = 2;")
        precio_teclado = cur.fetchone()[0]
        precio_esperado_teclado = Decimal('83.589')
        assert precio_teclado == precio_esperado_teclado, \
            f"Precio de 'Teclado' incorrecto. Esperado: {precio_esperado_teclado}, Obtenido: {precio_teclado}"

        cur.execute("SELECT precio FROM productos WHERE id = 3;")
        precio_mouse = cur.fetchone()[0]
        precio_esperado_mouse = Decimal('27.50')
        assert precio_mouse == precio_esperado_mouse, \
            f"Precio de 'Mouse' incorrecto. Esperado: {precio_esperado_mouse}, Obtenido: {precio_mouse}"

        cur.execute("CALL productos_por_rango(%s, %s, 'micursor');", (100, 500))

        cur.execute('FETCH ALL FROM "micursor";')

        resultados_rango = cur.fetchall()

        assert len(resultados_rango) == 4, f"Se esperaban 4 productos en el rango, pero se obtuvieron {len(resultados_rango)}."

        nombres_productos = [row[1] for row in resultados_rango]

        nombres_esperados = ['Router', 'Disco Duro', 'Silla', 'Monitor']

        assert nombres_productos == nombres_esperados, \
            f"Los productos devueltos o su orden no son correctos. Esperado: {nombres_esperados}, Obtenido: {nombres_productos}"

    finally:
        if conn:
            cur.close()
            conn.close()
        
