CREATE PROCEDURE insertar_producto(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO productos(nombre, precio)
    VALUES (nombre, precio);
END;
$$;

CALL insertar_producto('Tablet Android 10"', 3200.00);
CALL insertar_producto('Impresora Multifuncional Wi-Fi', 2899.00);
CALL insertar_producto('Silla Ergonómica de Oficina', 1899.50);
CALL insertar_producto('Router Wi-Fi 6 AX3000', 1450.00);
CALL insertar_producto('Cámara de Seguridad IP', 999.00);
CALL insertar_producto('Micrófono USB Profesional', 850.00);
CALL insertar_producto('Cargador Rápido USB-C 65W', 499.99);
CALL insertar_producto('Estabilizador de Voltaje 1000VA', 780.00);
CALL insertar_producto('Kit de Herramientas para PC', 350.00);
CALL insertar_producto('Panel LED RGB para Setup Gamer', 699.00);
