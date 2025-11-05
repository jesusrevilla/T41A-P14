import psycopg2

def test_procedures_run():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    # Probar eliminar_producto
    cur.execute("CALL eliminar_producto(9999);")  # No existe
    cur.execute("CALL eliminar_producto(1);")      # Sí existe

    # Probar aumentar_precios
    cur.execute("CALL aumentar_precios(10);")
    cur.execute("SELECT precio FROM productos;")
    precios = [p[0] for p in cur.fetchall()]
    assert all(p > 0 for p in precios)

    # Probar productos_en_rango
    cur.execute("CALL productos_en_rango(100, 2000);")

    # Probar actualizar_producto_audit
    cur.execute("CALL actualizar_producto_audit(2, 999.99);")
    cur.execute("SELECT COUNT(*) FROM auditoria;")
    count = cur.fetchone()[0]
    assert count >= 1

    cur.close()
    conn.close()