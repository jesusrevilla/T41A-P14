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

CREATE PROCEDURE eliminar_producto(
  IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos
    WHERE Id = p_Id;
    
    IF FOUND THEN
      RAISE NOTICE 'Producto eliminado';
    END IF;
END;
$$;

CALL eliminar_producto(1);

CREATE PROCEDURE productos_por_rango(
    p_precio_min NUMERIC,
    p_precio_max NUMERIC,
    INOUT p_cursor REFCURSOR 
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN p_cursor FOR
        SELECT
            p.id,
            p.nombre,
            p.precio
        FROM
            productos AS p
        WHERE
            p.precio BETWEEN p_precio_min AND p_precio_max
        ORDER BY
            p.precio;
END;
$$;

BEGIN;
CALL obtener_productos_por_rango_proc(100, 500, 'micursor');
FETCH ALL FROM "micursor";
COMMIT;
