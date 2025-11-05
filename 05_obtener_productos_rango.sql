-- Ejercicio 3: Devolver productos en un rango 
CREATE FUNCTION obtener_productos_por_rango(
    p_min NUMERIC,
    p_max NUMERIC
)
RETURNS TABLE(
    id_producto INT,
    nombre_producto TEXT,
    precio_producto NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    
    RETURN QUERY
    SELECT id, nombre, precio
    FROM productos
    WHERE precio >= p_min AND precio <= p_max
    ORDER BY precio;
END;
$$;
