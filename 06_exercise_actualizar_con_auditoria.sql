CREATE OR REPLACE PROCEDURE actualizar_precio(
    IN p_id INT,
    IN p_nuevo_precio NUMERIC,
    IN p_motivo TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_precio_anterior NUMERIC;
BEGIN
    IF p_nuevo_precio <= 0 THEN
        RAISE EXCEPTION 'El precio debe ser mayor que cero.';
    END IF;

    SELECT precio INTO v_precio_anterior
    FROM productos WHERE id = p_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Producto con id % no existe.', p_id;
    END IF;

    UPDATE productos
    SET precio = p_nuevo_precio
    WHERE id = p_id;

    INSERT INTO auditoria_precios(producto_id, precio_anterior, precio_nuevo, motivo)
    VALUES (p_id, v_precio_anterior, p_nuevo_precio, p_motivo);

    RAISE NOTICE 'Precio actualizado de % a % para producto %', v_precio_anterior, p_nuevo_precio, p_id;
END;
$$;
