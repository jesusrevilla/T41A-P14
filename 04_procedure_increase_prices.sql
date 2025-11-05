CREATE PROCEDURE porcentaje_precio(
    IN p_porcentaje NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET precio = precio + precio*p_porcentaje;
END;
$$;
CALL porcentaje_precio(0.1);

SELECT * FROM productos;