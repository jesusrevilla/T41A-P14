CREATE PROCEDURE borrar_por_id(product_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    filas_afectadas INT;
BEGIN
    DELETE FROM productos
    WHERE product_id = borrar_por_id.product_id;

    GET DIAGNOSTICS filas_afectadas = ROW_COUNT;

    IF filas_afectadas > 0 THEN
        RAISE NOTICE 'Producto eliminado exitosamente.';
    ELSE
        RAISE NOTICE 'No se encontró ningún producto con ese ID.';
    END IF;
END;
$$;
