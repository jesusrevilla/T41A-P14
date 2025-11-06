CREATE PROCEDURE porcentaje_producto(
    IN porcentaje NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos 
    SET precio= precio+(precio*(porcentaje/100.0));
END;
$$;
