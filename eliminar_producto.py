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
