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
