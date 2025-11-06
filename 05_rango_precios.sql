CREATE PROCEDURE rango_precio(
  IN precio_min NUMERIC,
  IN precio_max NUMERIC,
  OUT Lista_p TEXT
)
LANGUAGE plpgsql
As $$
BEGIN
  SELECT STRING_AGG(nombre,', ') INTO Lista_p
  FROM productos
  WHERE precio BETWEEN precio_min AND precio_max;
END;
$$;
