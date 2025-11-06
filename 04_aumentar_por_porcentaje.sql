--Crear un procedimiento que recorra todos los productos y aumente su precio en un porcentaje dado
CREATE PROCEDURE aumenta_precio(
  IN p_percentage NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
  IF EXISTS(SELECT 1 FROM productos) THEN
    UPDATE productos SET precio=precio+(precio/100*p_percentage);
    RAISE NOTICE 'Productos aumentados %%% correctamente',p_percentage;
  ELSE
    RAISE NOTICE 'Error en aumentar precio';
  END IF;
END;
$$;
