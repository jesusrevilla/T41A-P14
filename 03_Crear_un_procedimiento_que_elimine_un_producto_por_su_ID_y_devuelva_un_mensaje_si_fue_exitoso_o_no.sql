CREATE PROCEDURE eliminar_producto(
    IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos
    WHERE id = p_id;

    IF FOUND THEN
        RAISE NOTICE 'Producto con ID % eliminado correctamente.', p_id;
    ELSE
        RAISE NOTICE 'No se encontró producto con ID %.', p_id;
    END IF;
END;
$$;

-- Ejemplo de llamada:
CALL eliminar_producto(2);
