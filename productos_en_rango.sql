-- Muestra productos dentro de un rango de precios
CREATE PROCEDURE productos_en_rango(
    IN precio_min NUMERIC,
    IN precio_max NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    RAISE NOTICE 'Productos entre % y %:', precio_min, precio_max;
    FOR producto IN
        SELECT * FROM productos
        WHERE precio BETWEEN precio_min AND precio_max
    LOOP
        RAISE NOTICE 'ID: %, Nombre: %, Precio: %', producto.id, producto.nombre, producto.precio;
    END LOOP;
END;
$$;

CALL productos_en_rango(100, 500);
