CREATE OR REPLACE PROCEDURE eliminar_producto(IN p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos
    WHERE id = p_id;

    IF FOUND THEN
        RAISE NOTICE 'Producto eliminado correctamente.';
    ELSE
        RAISE NOTICE 'No se encontró el producto';
    END IF;
END;
$$;


CALL eliminar_producto(3);
