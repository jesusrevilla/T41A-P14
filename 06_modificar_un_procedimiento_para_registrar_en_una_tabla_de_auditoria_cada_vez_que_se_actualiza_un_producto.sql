CREATE PROCEDURE actualizar_precio_audit(
    IN p_id INT,
    IN p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_precio NUMERIC;
BEGIN
    SELECT precio INTO v_precio
    FROM productos
    WHERE id = p_id;

    IF p_nuevo_precio > 0 THEN
        UPDATE productos
        SET precio = p_nuevo_precio
        WHERE id = p_id;

        INSERT INTO auditoria_productos(producto_id, precio_anterior, precio_nuevo)
        VALUES (p_id, v_precio, p_nuevo_precio);

        RAISE NOTICE 'Precio actualizado y registrado en auditoría.';
    ELSE
        RAISE NOTICE 'El precio debe ser mayor que cero.';
    END IF;
END;
$$;

-- Ejemplo de llamada:
CALL actualizar_precio_audit(1, 500.00);
