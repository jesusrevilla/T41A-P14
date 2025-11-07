CREATE OR REPLACE PROCEDURE aumentar_precios(
    IN p_porcentaje NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET precio = precio + (precio * p_porcentaje / 100);

    RAISE NOTICE 'Precios aumentados';
END;
$$;

CALL aumentar_precios(10);
