-- Ejercicio 2: Recorrer y aumentar precios
CREATE PROCEDURE aumentar_precios_porcentaje(IN p_porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
BEGIN
    -- Validar que el porcentaje sea positivo
    IF p_porcentaje <= 0 THEN
        RAISE NOTICE 'El porcentaje debe ser mayor que cero.';
        RETURN; 
    END IF;

    -- Bucle FOR que recorre el resultado de un SELECT
    FOR rec IN SELECT * FROM productos
    LOOP
        
        UPDATE productos
        SET precio = rec.precio * (1 + (p_porcentaje / 100))
        WHERE id = rec.id;
    END LOOP;
    
    RAISE NOTICE 'Precios actualizados en un % %% exitosamente.', p_porcentaje;
END;
$$;
