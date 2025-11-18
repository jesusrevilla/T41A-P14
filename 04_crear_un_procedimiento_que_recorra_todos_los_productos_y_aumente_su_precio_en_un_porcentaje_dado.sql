CREATE PROCEDURE aumentar_precio(
    IN p_porcentaje NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET precio = precio + (precio * p_porcentaje / 100);

    RAISE NOTICE 'Se aumentaron los precios en % %.', p_porcentaje, '%';
END;
$$;

-- Ejemplo de llamada:
CALL aumentar_precio(10);
