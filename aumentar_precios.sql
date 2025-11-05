-- Aumenta el precio de todos los productos en un porcentaje dado
CREATE PROCEDURE aumentar_precios(
    IN porcentaje NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE productos
    SET precio = precio + (precio * porcentaje / 100);
    RAISE NOTICE 'Precios actualizados en un %', porcentaje;
END;
$$;

CALL aumentar_precios(10);
