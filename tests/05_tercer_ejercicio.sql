CREATE PROCEDURE sp_mostrar_productos_por_rango(
    p_inicio DECIMAL(10, 2),
    p_fin DECIMAL(10, 2)
)
LANGUAGE plpgsql
AS $$
DECLARE
 
    v_producto RECORD; 
BEGIN
   
    RAISE NOTICE '--- Productos encontrados entre % y % ---', p_inicio, p_fin;

    FOR v_producto IN
        SELECT nombre, precio 
        FROM productos 
        WHERE precio >= p_inicio AND precio <= p_fin
        ORDER BY precio
    LOOP
       
        RAISE NOTICE 'Producto: %, Precio: $%', 
                     v_producto.nombre, 
                     v_producto.precio;
    END LOOP;

    RAISE NOTICE '--- Fin del reporte ---';
END;
$$;

CALL sp_mostrar_productos_por_rango(20.00, 200.00);
