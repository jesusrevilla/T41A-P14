-- Procedimiento que elimina un producto por su ID y devuelve un mensaje
CREATE OR REPLACE PROCEDURE eliminar_producto(producto_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    existe BOOLEAN;
BEGIN
    SELECT EXISTS(SELECT 1 FROM productos WHERE id = producto_id) INTO existe;

    IF existe THEN
        DELETE FROM productos WHERE id = producto_id;
        RAISE NOTICE 'Producto con ID % eliminado exitosamente.', producto_id;
    ELSE
        RAISE NOTICE 'No se encontró ningún producto con el ID %. No se realizó ninguna eliminación.', producto_id;
    END IF;
END;
$$;



