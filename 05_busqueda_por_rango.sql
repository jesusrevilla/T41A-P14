--Crear un procedimiento que reciba un rango de precios y devuelva los productos dentro de ese rango.

CREATE OR REPLACE FUNCTION busqueda_por_rango(p_rangoI NUMERIC, p_rangoF NUMERIC)
RETURNS TABLE(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT p.nombre, p.precio
  FROM productos p
  WHERE p.precio > p_rangoI AND p.precio < p_rangoF;
END;
$$;
