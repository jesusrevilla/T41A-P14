CREATE PROCEDURE eliminar_id(IN p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM productos WHERE id=p_id) THEN
    DELETE FROM productos WHERE id=p_id;
    RAISE NOTICE 'El producto con id:% ha sido eliminado exitosamente',p_id;
  ELSE
    RAISE NOTICE 'El producto no se encuentra en la lista, error';
  END IF;
END;
$$;
