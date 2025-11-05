CREATE OR REPLACE PROCEDURE aumentar_precios(IN porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    IF porcentaje <= 0 THEN
        RAISE NOTICE 'El porcentaje debe ser mayor que cero.';
        RETURN;
    END IF;

    UPDATE productos
    SET precio = precio + (precio * porcentaje / 100);

    RAISE NOTICE 'Precios aumentados en % %', porcentaje, '%';
END;
$$;