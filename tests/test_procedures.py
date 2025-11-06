import decimal
import uuid
import psycopg2

DBCFG = dict(
    dbname='test_db',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

def connect():
    return psycopg2.connect(**DBCFG)

def test_eliminar_producto_deletes_row():
    conn = connect()
    cur = conn.cursor()
    try:
        name = f"Temporal_{uuid.uuid4().hex[:8]}"
        cur.execute("INSERT INTO productos(nombre, precio) VALUES (%s, %s) RETURNING id;", (name, decimal.Decimal('123.45')))
        prod_id = cur.fetchone()[0]
        cur.execute("CALL eliminar_producto(%s, NULL);", (prod_id,))
        cur.execute("SELECT COUNT(*) FROM productos WHERE id=%s;", (prod_id,))
        assert cur.fetchone()[0] == 0
        conn.commit()
    finally:
        cur.close()
        conn.close()

def test_actualizar_precio_creates_audit():
    conn = connect()
    cur = conn.cursor()
    try:
        name = f"Actualizable_{uuid.uuid4().hex[:8]}"
        cur.execute("INSERT INTO productos(nombre, precio) VALUES (%s, %s) RETURNING id, precio;", (name, decimal.Decimal('100.00')))
        prod_id, old_price = cur.fetchone()

        cur.execute("CALL actualizar_precio(%s, %s, %s);", (prod_id, decimal.Decimal('150.00'), "ajuste de prueba"))
        cur.execute("SELECT precio FROM productos WHERE id=%s;", (prod_id,))
        assert cur.fetchone()[0] == decimal.Decimal('150.00')

        cur.execute("SELECT precio_anterior, precio_nuevo, motivo FROM auditoria_precios WHERE producto_id=%s ORDER BY cambiado_en DESC LIMIT 1;", (prod_id,))
        row = cur.fetchone()
        assert row[0] == decimal.Decimal('100.00')
        assert row[1] == decimal.Decimal('150.00')
        assert row[2] == "ajuste de prueba"
        conn.commit()
    finally:
        cur.close()
        conn.close()

def test_aumentar_precios_porcentaje_in_transaction():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COALESCE(SUM(precio), 0) FROM productos;")
        s_before = cur.fetchone()[0]

        cur.execute("CALL aumentar_precios_porcentaje(%s);", (decimal.Decimal('10.0'),))
        cur.execute("SELECT COALESCE(SUM(precio), 0) FROM productos;")
        s_after = cur.fetchone()[0]

        expected = (s_before * decimal.Decimal('1.10')).quantize(decimal.Decimal('0.01'))
        assert s_after.quantize(decimal.Decimal('0.01')) == expected
        conn.rollback()  # revertir cambios globales
    finally:
        cur.close()
        conn.close()

def test_productos_en_rango_returns_expected():
    conn = connect()
    cur = conn.cursor()
    names = [f"Rango50_{uuid.uuid4().hex[:6]}", f"Rango150_{uuid.uuid4().hex[:6]}", f"Rango300_{uuid.uuid4().hex[:6]}"]
    try:
        cur.execute("INSERT INTO productos(nombre, precio) VALUES (%s, %s) RETURNING id;", (names[0], decimal.Decimal('50.00')))
        id50 = cur.fetchone()[0]
        cur.execute("INSERT INTO productos(nombre, precio) VALUES (%s, %s) RETURNING id;", (names[1], decimal.Decimal('150.00')))
        id150 = cur.fetchone()[0]
        cur.execute("INSERT INTO productos(nombre, precio) VALUES (%s, %s) RETURNING id;", (names[2], decimal.Decimal('300.00')))
        id300 = cur.fetchone()[0]
        conn.commit()

        cur.execute("BEGIN;")
        cur.execute("CALL productos_en_rango(%s, %s, %s);", (decimal.Decimal('100.00'), decimal.Decimal('250.00'), 'c1'))
        cur.execute("FETCH ALL FROM c1;")
        rows = cur.fetchall()
        cur.execute("COMMIT;")

        returned_names = {r[1] for r in rows}
        assert names[1] in returned_names
        assert names[0] not in returned_names
        assert names[2] not in returned_names
    finally:
        try:
            cur.execute("DELETE FROM productos WHERE nombre = ANY(%s);", (names,))
            conn.commit()
        except Exception:
            conn.rollback()
        cur.close()
        conn.close()
