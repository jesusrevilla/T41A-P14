CREATE PROCEDURE sp_mostrar_productos_por_rango(
    p_bot DECIMAL(10, 2),
    p_top DECIMAL(10, 2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_producto RECORD; 
BEGIN
    FOR v_producto IN
        SELECT nombre, precio 
        FROM productos 
        WHERE precio >= p_bot AND precio <= p_top
        ORDER BY precio
    LOOP
        RAISE NOTICE 'Producto: %, Precio: $%', 
                     v_producto.nombre, 
                     v_producto.precio;
    END LOOP;

END;
$$;

CALL sp_mostrar_productos_por_rango(500.00, 1000.00);
