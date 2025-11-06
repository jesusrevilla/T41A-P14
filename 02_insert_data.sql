CREATE PROCEDURE insertar_producto(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO productos(nombre, precio)
    VALUES (nombre, precio);
END;
$$;

CALL insertar_producto('Teclado', 299.99);
CALL insertar_producto('Raton', 99.99);
CALL insertar_producto('Camara', 1099.99);
--select * from productos;
