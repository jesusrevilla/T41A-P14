CREATE OR REPLACE PROCEDURE eliminar_producto(
    IN p_id INT,
    OUT p_mensaje TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_nombre TEXT;
BEGIN
    SELECT nombre INTO v_nombre FROM productos WHERE id = p_id;
    IF NOT FOUND THEN
        p_mensaje := format('No existe el producto con id %s', p_id);
        RAISE NOTICE '%', p_mensaje;
        RETURN;
    END IF;

    DELETE FROM productos WHERE id = p_id;
    p_mensaje := format('Producto "%s" (id=%s) eliminado correctamente', v_nombre, p_id);
    RAISE NOTICE '%', p_mensaje;
END;
$$;
