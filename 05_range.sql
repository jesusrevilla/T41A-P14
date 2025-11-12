CREATE OR REPLACE FUNCTION busqueda_por_rango(p_rangoI NUMERIC, p_rangoF NUMERIC)
RETURNS TABLE(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT productos.nombre, productos.precio
  FROM productos
  WHERE productos.precio > p_rangoI AND productos.precio < p_rangoF;
END;
$$;
