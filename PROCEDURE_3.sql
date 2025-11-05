CREATE PROCEDURE rango_precio(
    IN rango_i NUMERIC,
    IN rango_s NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
   FOR r IN
    SELECT nombre
    FROM productos
    WHERE precio BETWEEN rango_i AND rango_s 
    LOOP
        RAISE NOTICE 'Producto: %', r.nombre;
    END LOOP;
END;
$$;
