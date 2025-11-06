CREATE PROCEDURE eliminar_producto(
    IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM productos WHERE id = p_id) THEN
        Delete from productos
        WHERE id = p_id;
        RAISE NOTICE 'Se elimino el producto exitosamente.';
    ELSE 
        RAISE NOTICE 'No se encontro el producto';
    END IF;
END;
$$;

CALL eliminar_productos(2);
CALL eliminar_productos(15);

