-- Eliminar un producto por ID
CREATE PROCEDURE eliminar_producto(IN p_id_producto INT)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Intenta eliminar el producto con el ID dado
    DELETE FROM productos WHERE id = p_id_producto;
    IF FOUND THEN
        RAISE NOTICE 'Producto % eliminado exitosamente.', p_id_producto;
    ELSE
        RAISE NOTICE 'Error: No se encontró el producto con ID %.', p_id_producto;
    END IF;
END;
$$;
