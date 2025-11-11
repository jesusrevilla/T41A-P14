CREATE PROCEDURE insertar_producto(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO productos(nombre, precio)
    VALUES (nombre, precio);
END;
$$;

CALL insertar_producto('Teclado', 299.99);
CALL insertar_producto('Mouse Inalámbrico', 199.50);
CALL insertar_producto('Monitor Curvo 32"', 5499.00);
CALL insertar_producto('Laptop Core i7 16GB RAM', 17500.00);
CALL insertar_producto('Disco SSD NVMe 1TB', 1650.00);
CALL insertar_producto('Memoria RAM 16GB DDR4', 1100.00);
CALL insertar_producto('Tarjeta Gráfica RTX 4060', 8990.00);
CALL insertar_producto('Webcam 1080p con Micrófono', 750.00);
CALL insertar_producto('Hub USB-C 5-en-1', 450.00);
CALL insertar_producto('Disco Duro Externo 4TB', 2300.00);
CALL insertar_producto('Audífonos con Cancelación de Ruido', 1299.99);
