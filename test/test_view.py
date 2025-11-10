def test_borrar_producto(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM catalogo_productos WHERE producto_id = 1;")
        assert cur.fetchone()[0] == 1

        cur.execute("CALL borrar_producto(1);")

        cur.execute("SELECT COUNT(*) FROM catalogo_productos WHERE producto_id = 1;")
        assert cur.fetchone()[0] == 0

def test_ajustar_precios(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT precio_unitario FROM catalogo_productos WHERE nombre_producto = 'Mouse';")
        precio_original = cur.fetchone()[0]

        cur.execute("CALL ajustar_precios(10);")

        cur.execute("SELECT precio_unitario FROM catalogo_productos WHERE nombre_producto = 'Mouse';")
        precio_nuevo = cur.fetchone()[0]

        assert round(precio_nuevo, 2) == round(precio_original * Decimal('1.10'), 2)

def test_listar_productos_por_precio(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT nombre_producto FROM catalogo_productos
            WHERE precio_unitario BETWEEN 50 AND 200 ORDER BY precio_unitario;
        """)
        nombres = [r[0] for r in cur.fetchall()]

        assert "Mouse" in nombres
        assert "Auriculares" in nombres
