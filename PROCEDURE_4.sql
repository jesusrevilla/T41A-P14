CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INT NOT NULL,
    precio_anterior NUMERIC,
    precio_nuevo NUMERIC
);

CREATE OR REPLACE PROCEDURE actualizar_precio(
    IN p_id INT,
    IN p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_precio_anterior NUMERIC;
BEGIN
    SELECT precio INTO v_precio_anterior
    FROM productos
    WHERE id = p_id;
    IF FOUND THEN
        UPDATE productos
        SET precio = p_nuevo_precio
        WHERE id = p_id;
        INSERT INTO auditoria_productos (producto_id, precio_anterior, precio_nuevo)
        VALUES (p_id, v_precio_anterior, p_nuevo_precio);
    ELSE
        RAISE NOTICE 'Producto con ID % no encontrado.', p_id;
    END IF;
END;
$$;
