CREATE PROCEDURE actualizar_precio_segun_porcentaje(
    IN porcentaje FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos SET precio = precio * ((100+porcentaje)/100);
END;
$$;

CALL actualizar_precio_segun_porcentaje(10);
