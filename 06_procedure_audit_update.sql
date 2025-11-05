CREATE OR REPLACE PROCEDURE actualizar_producto_audit(
    IN p_id INT,
    IN p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_nuevo_precio > 0 THEN
        UPDATE productos
        SET precio = p_nuevo_precio
        WHERE id = p_id;

        INSERT INTO auditoria (producto_id, accion)
        VALUES (p_id, 'Actualización de precio');

        RAISE NOTICE 'Producto % actualizado y registrado en auditoría.', p_id;
    ELSE
        RAISE NOTICE 'El precio debe ser mayor que cero.';
    END IF;
END;
$$;