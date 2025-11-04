\echo '=== TEST ==='

\echo '1. Estado inicial de la base de datos:'
SELECT id, nombre, precio FROM productos ORDER BY id;

\echo '2. Ejecutando aumentar_precios_porcentaje(15):'
CALL aumentar_precios_porcentaje(15);

\echo '3. Ejecutando obtener_productos_por_rango_precio(150, 2000):'
DO $$
DECLARE
    cur REFCURSOR;
    producto_record RECORD;
BEGIN
    CALL obtener_productos_por_rango_precio(150, 2000, cur);
    LOOP
        FETCH cur INTO producto_record;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Producto: % - Precio: %', producto_record.nombre, producto_record.precio;
    END LOOP;
    CLOSE cur;
END $$;

\echo '4. Ejecutando actualizar_producto_con_auditoria:'
CALL actualizar_producto_con_auditoria(3, 'Monitor LED', 1500.00);

\echo '5. Estado final de productos:'
SELECT id, nombre, precio FROM productos ORDER BY id;

\echo '6. Registros de auditoría generados:'
SELECT * FROM auditoria_productos ORDER BY fecha_cambio;
