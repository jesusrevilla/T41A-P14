CREATE PROCEDURE eliminar_producto(
    IN p_id INT,
    OUT p_mensaje TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos
    WHERE id = p_id;

    IF FOUND THEN
        p_mensaje := format('Producto eliminado correctamente.');
    ELSE
        p_mensaje := format('No se encontro el producto');
    END IF;
END;
$$;

CALL eliminar_producto(3, NULL);
