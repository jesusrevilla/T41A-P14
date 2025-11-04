CREATE PROCEDURE eliminar_producto(
    p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos
    WHERE id = p_id;

    IF FOUND THEN
        RAISE NOTICE 'Producto eliminado exitosamente (ID: %)', p_id;
    ELSE
        RAISE NOTICE 'Error: No se encontró un producto con el ID %.', p_id;
    END IF;
END;
$$;
