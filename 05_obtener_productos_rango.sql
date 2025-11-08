CREATE OR REPLACE FUNCTION obtener_productos_rango(precio_min NUMERIC, precio_max NUMERIC)
RETURNS TABLE(id INT, nombre VARCHAR, precio NUMERIC, stock INT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, nombre, precio, stock
    FROM productos
    WHERE precio BETWEEN precio_min AND precio_max
    ORDER BY precio ASC;
END;
$$ LANGUAGE plpgsql;
