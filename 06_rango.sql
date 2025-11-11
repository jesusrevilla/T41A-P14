CREATE OR REPLACE PROCEDURE productos_en_rango(IN p_min NUMERIC, IN p_max NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE NOTICE 'Productos en el rango de % a %:', p_min, p_max;

    FOR record IN
        SELECT * FROM productos WHERE precio BETWEEN p_min AND p_max
    LOOP
        RAISE NOTICE '% - $%', record.nombre, record.precio;
    END LOOP;
END;
$$;
