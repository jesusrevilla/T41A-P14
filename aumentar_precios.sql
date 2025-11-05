CREATE PROCEDURE aumentar_precios(
  IN p_porcentaje NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE 
   aumento NUMERIC;
BEGIN
  IF p_porcentaje <=0 THEN
    RAISE NOTICE 'Ingresa porcentaje mayor a cero';
    RETURN;
  END IF;
  
  aumento :=1.0+(p_porcentaje/100.0);
  UPDATE productos
  SET precio=precio*aumento;
  
  IF FOUND THEN
    RAISE NOTICE 'Se actualizaron los precios';
  ELSE
    RAISE NOTICE 'No se actualizaron por que no hay datos';
  END IF;
  
END;
$$;

CALL aumentar_precios(10);
