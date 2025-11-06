CREATE PROCEDURE insertar_producto(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO productos(nombre, precio)
  VALUES (nombre, precio);
END;
$$;

CALL insertar_producto('Teclado', 199.99);
CALL insertar_producto('Raton', 99.99);
CALL insertar_producto('Caja', 9.99);
CALL insertar_producto('Monitor', 299.99);
CALL insertar_producto('CPU', 499.99);
