CREATE PROCEDURE insertar_registro(nombre TEXT, stock INT, precio_unitario NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO productos(nombre, stock, precio_unitario)
  VALUES (nombre, stock, precio_unitario);
END;
$$;

CALL insertar_registro('Teclado', 5, 199.99);
CALL insertar_registro('Raton', 10, 99.99);
CALL insertar_registro('Caja', 2, 9.99);
CALL insertar_registro('Monitor', 6, 299.99);
CALL insertar_registro('CPU', 3, 499.99);
