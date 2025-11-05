-- Actualiza el precio de un producto y registra el cambio en la auditoría
CREATE PROCEDURE actualizar_precio_auditado(
    IN p_id INT,
    IN p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql AS $$
DECLARE
    precio_actual NUMERIC;
BEGIN
    SELECT precio INTO precio_actual FROM productos WHERE id = p_id;

    IF NOT FOUND THEN
        RAISE NOTICE 'Producto no encontrado.';
        RETURN;
    END IF;

    IF p_nuevo_precio > 0 THEN
        UPDATE productos
        SET precio = p_nuevo_precio
        WHERE id = p_id;

        INSERT INTO auditoria_productos(producto_id, precio_anterior, precio_nuevo)
        VALUES (p_id, precio_actual, p_nuevo_precio);

        RAISE NOTICE 'Precio actualizado y registrado en auditoría.';
    ELSE
        RAISE NOTICE 'El precio debe ser mayor que cero.';
    END IF;
END;
$$;

CALL actualizar_precio_auditado(5, 450.00);
