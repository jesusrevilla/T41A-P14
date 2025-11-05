CREATE PROCEDURE insertar_producto(nombre TEXT, precio NUMERIC) LANGUAGE plpgsql 
AS $$ 
BEGIN 
  INSERT INTO productos(nombre, precio) 
  VALUES (nombre, precio); 
END;
$$;

CALL insertar_producto('Tablet Android 10.1"', 3899.00);
CALL insertar_producto('Impresora Multifuncional WiFi', 2499.00);
CALL insertar_producto('Router WiFi 6 AX3000', 1890.00);
CALL insertar_producto('Cámara de Seguridad IP', 1350.00);
CALL insertar_producto('Cargador Rápido USB-C 65W', 599.00);
CALL insertar_producto('Estabilizador de Voltaje 1000VA', 850.00);
CALL insertar_producto('Silla Ergonómica para Oficina', 3299.00);
CALL insertar_producto('Soporte Ajustable para Laptop', 399.00);
CALL insertar_producto('Kit de Herramientas para PC', 299.00);
CALL insertar_producto('Micrófono Condensador USB', 899.00);
CALL insertar_producto('Panel LED RGB para Setup Gamer', 499.00);
CALL insertar_producto('Controlador Bluetooth para Juegos', 799.00);
CALL insertar_producto('Pantalla Interactiva Táctil 24"', 6999.00);
CALL insertar_producto('Kit de Limpieza para Electrónicos', 199.00);
CALL insertar_producto('Fuente de Poder 750W Certificada', 1450.00);
