-- 3_Crear una FUNCIÓN que reciba un rango de precios y devuelva los productos dentro de ese rango.
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
