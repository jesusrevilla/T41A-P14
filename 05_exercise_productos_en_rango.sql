

DROP PROCEDURE IF EXISTS productos_en_rango(NUMERIC, NUMERIC, REFCURSOR);
CREATE PROCEDURE productos_en_rango(
  p_min NUMERIC,
  p_max NUMERIC,
  INOUT p_cursor REFCURSOR
)
LANGUAGE plpgsql
AS $$
BEGIN
  -- Si no mandan nombre, usa uno por defecto (no afecta al test)
  IF p_cursor IS NULL OR p_cursor = '' THEN
    p_cursor := 'productos_en_rango_cur';
  END IF;

  OPEN p_cursor FOR
    SELECT id, nombre, precio FROM productos
     WHERE precio BETWEEN p_min AND p_max ORDER BY id;
END;
$$;
