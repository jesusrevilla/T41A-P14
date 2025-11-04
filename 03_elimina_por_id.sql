CREATE PROCEDURE eliminar_producto(
    IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM productos WHERE id = p_id) THEN
        Delete from productos
        WHERE id = p_id;
        RAISE NOTICE 'Se elimino el producto.';
    END IF;
END;
$$;
--CALL eliminar_producto (2);
--select * from productos;
