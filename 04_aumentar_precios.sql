CREATE PROCEDURE aumentar_precios(
    IN p_porcentaje NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_porcentaje <= 0 THEN
        RAISE NOTICE 'El porcentaje debe ser mayor que cero.';
        RETURN;
    END IF;

    UPDATE productos
    SET precio = precio + (precio * p_porcentaje / 100);

    RAISE NOTICE 'Precios aumentados';
END;
$$;

CALL aumentar_precios(10);
