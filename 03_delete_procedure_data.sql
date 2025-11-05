-- Procedimiento para eliminar un producto por su ID

CREATE OR REPLACE PROCEDURE eliminar_producto(IN p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM productos WHERE id = p_id) THEN
        DELETE FROM productos WHERE id = p_id;
        RAISE NOTICE 'Producto con ID % eliminado exitosamente.', p_id;
    ELSE
        RAISE NOTICE 'No existe producto con ID %.', p_id;
    END IF;
END;
$$;
