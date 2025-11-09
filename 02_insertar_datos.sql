CREATE PROCEDURE insertar_producto(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO productos(nombre, precio)
  VALUES (nombre, precio);
END;
$$;

CALL insertar_producto('Laptop', 15000.00);
CALL insertar_producto('Mouse', 350.00);
CALL insertar_producto('Teclado', 700.00);
CALL insertar_producto('Monitor', 4200.00);
CALL insertar_producto('USB', 200.00);
