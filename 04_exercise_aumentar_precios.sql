CREATE OR REPLACE PROCEDURE aumentar_precios_porcentaje(IN p_porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    v_factor NUMERIC;
    v_updated INT;
BEGIN
    IF p_porcentaje <= -100 THEN
        RAISE EXCEPTION 'El porcentaje no puede ser <= -100%%';
    END IF;

    v_factor := 1 + (p_porcentaje / 100.0);
    UPDATE productos
       SET precio = ROUND(precio * v_factor, 2);
    GET DIAGNOSTICS v_updated = ROW_COUNT;
    RAISE NOTICE 'Se actualizaron % filas con factor %', v_updated, v_factor;
END;
$$;
