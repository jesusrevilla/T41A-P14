CREATE PROCEDURE eliminar_producto(
    IN p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS(   
    SELECT
      id
    FROM
      productos
    WHERE
      id=p_id) THEN 
    DELETE FROM productos
    WHERE id=p_id;
     RAISE NOTICE 'Borrado con exito.';
    ELSE
        RAISE NOTICE 'No se encuentra el ID en la lista.';
    END IF;
END;
$$;
CALL eliminar_producto(1);
SELECT * FROM productos;
