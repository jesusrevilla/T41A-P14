-- Elimina un producto por su ID y devuelve un mensaje
CREATE PROCEDURE eliminar_producto(
    IN p_id INT,
    OUT mensaje TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM productos WHERE id = p_id) THEN
        DELETE FROM productos WHERE id = p_id;
        mensaje := 'Producto eliminado exitosamente.';
    ELSE
        mensaje := 'Producto no encontrado.';
    END IF;
END;
$$;

CALL eliminar_producto(10, NULL);
