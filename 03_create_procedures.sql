CREATE PROCEDURE eliminar_producto(
    IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_id IN  THEN
        UPDATE productos
        SET precio = p_nuevo_precio
        WHERE id = p_id;
    ELSE
        RAISE NOTICE 'El precio debe ser mayor que cero.';
    END IF;
END;
$$;
