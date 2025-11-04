CREATE PROCEDURE eliminar_producto(
    IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos WHERE id=p_id;
END;
$$;

CALL eliminar_producto(1);
