CREATE OR REPLACE PROCEDURE productos_rango(
    IN p_min NUMERIC,
    IN p_max NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    prod RECORD;
BEGIN
    FOR prod IN
        SELECT * FROM productos
        WHERE precio BETWEEN p_min AND p_max
    LOOP
        RAISE NOTICE 'ID: %, Nombre: %, Precio: %',
                     prod.id, prod.nombre, prod.precio;
    END LOOP;
END;
$$;

CALL productos_rango(300, 8500);
