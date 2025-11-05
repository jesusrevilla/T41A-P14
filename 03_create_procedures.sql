CREATE PROCEDURE eliminar_producto(IN p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos where id=p_id;
    IF NOT FOUND THEN
      RAISE NOTICE 'id incorrecto';
    ELSE
      RAISE NOTICE 'eliminado correctamente';
    END IF;
END;
$$;

CREATE PROCEDURE actualizar_precio(IN porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    IF porcentaje IS NULL OR porcentaje < 0 THEN
        RAISE EXCEPTION 'El porcentaje de actualización debe ser un valor positivo.';
    END IF;
    UPDATE productos set precio=precio*(1+porcentaje);
END;
$$;

CREATE PROCEDURE rango_precios(
    IN inferior NUMERIC,
    IN superior NUMERIC,
    OUT lista TEXT
    )
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COALESCE(
        STRING_AGG(nombre, '|' ORDER BY nombre), --se agrupan los nombres de los productos
        'NO_RESULTADOS' -- si no hay resultados
    )
    INTO lista
    FROM productos
    WHERE precio BETWEEN inferior AND superior;
END;
$$;


