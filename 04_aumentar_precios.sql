CREATE OR REPLACE PROCEDURE aumentar_precios(porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET precio = precio + (precio * (porcentaje / 100));

    RAISE NOTICE 'Se han aumentado los precios en un % porcentaje.', porcentaje;
END;
$$;
