CREATE OR REPLACE PROCEDURE actualizar_precio_auditado(
    IN p_id INT,
    IN p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_precio_actual NUMERIC;
BEGIN
    SELECT precio INTO v_precio_actual FROM productos WHERE id = p_id;

    IF NOT FOUND THEN
        RAISE NOTICE 'No se encontró el producto';
        RETURN;
    END IF;

    IF p_nuevo_precio <= 0 THEN
        RAISE NOTICE 'El precio debe ser mayor que cero';
        RETURN;
    END IF;

    UPDATE productos
    SET precio = p_nuevo_precio
    WHERE id = p_id;

    INSERT INTO auditoria_productos(producto_id, accion)
    VALUES (p_id, format('Actualización de precio'));

    RAISE NOTICE 'Precio actualizado';
    RAISE NOTICE 'Registro insertado en auditoría';
END;
$$;

CALL actualizar_precio_auditado(2, 120.00);
