
-- Crear la tabla de productos si no existe

DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS auditoria_productos CASCADE; -- Nueva tabla para el Ejercicio 4

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC NOT NULL
);

CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INT NOT NULL,
    precio_anterior NUMERIC,
    precio_nuevo NUMERIC,
    fecha_modificacion TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);



-- Datos de prueba
-- Se limpia la tabla y se reinsertan los datos para asegurar un estado inicial conocido

INSERT INTO productos (nombre, precio) VALUES
('Laptop Pro', 1200.00),         -- ID 1
('Mouse Ergonomico', 35.50),     -- ID 2
('Monitor 4K', 450.00),          -- ID 3
('Teclado Mecanico', 80.00),     -- ID 4
('Webcam HD', 150.00),           -- ID 5
('Disco Externo 1TB', 60.00);    -- ID 6

SELECT '--- TABLA INICIAL ---' AS Test;
SELECT * FROM productos ORDER BY id;



-- PRUEBAS EJERCICIO 1: eliminar_producto

SELECT '--- PRUEBA 1.1: Eliminar Producto Existente (ID 3 - Monitor 4K) ---' AS Test;
DO $$ DECLARE v_mensaje TEXT; BEGIN CALL eliminar_producto(3, v_mensaje); RAISE NOTICE 'Resultado: %', v_mensaje; END $$;
SELECT 'Producto ID 3 debe haber desaparecido:' AS Check;
SELECT * FROM productos WHERE id = 3; -- Debe devolver 0 filas

SELECT '--- PRUEBA 1.2: Intentar Eliminar Producto Inexistente (ID 99) ---' AS Test;
DO $$ DECLARE v_mensaje TEXT; BEGIN CALL eliminar_producto(99, v_mensaje); RAISE NOTICE 'Resultado: %', v_mensaje; END $$;



-- PRUEBAS EJERCICIO 2: aumentar_precio_por_porcentaje

SELECT '--- PRUEBA 2.1: Aumentar Precio en 10% ---' AS Test;
CALL aumentar_precio_por_porcentaje(10.0);
SELECT 'Precios después del aumento del 10% (Ej: Laptop Pro debe ser 1320.00):' AS Check;
SELECT id, nombre, precio FROM productos ORDER BY id;



-- PRUEBAS EJERCICIO 3: obtener_productos_por_rango 

SELECT '--- PRUEBA 3.1: Productos en Rango [50.00 - 100.00] ---' AS Test;
-- Esperados: Disco Externo (66.00) y Teclado Mecanico (88.00)
SELECT * FROM obtener_productos_por_rango(50.00, 100.00);

SELECT '--- PRUEBA 3.2: Productos en Rango [300.00 - 1500.00] ---' AS Test;
-- Esperados: Laptop Pro (1320.00)
SELECT * FROM obtener_productos_por_rango(300.00, 1500.00);


-- PRUEBAS EJERCICIO 4: actualizar_precio_con_auditoria

SELECT '--- PRUEBA 4.1: Actualizar Producto ID 5 (Webcam HD) de 150.00 a 175.00 ---' AS Test;
SELECT 'Auditoría inicial (debe estar vacía):' AS Check;
SELECT * FROM auditoria_productos;

CALL actualizar_precio_con_auditoria(5, 175.00);

SELECT 'Precio actualizado en tabla productos (ID 5 debe ser 175.00):' AS Check;
SELECT * FROM productos WHERE id = 5;

SELECT 'Registro de auditoría (debe tener 1 fila):' AS Check;
-- Debe mostrar producto_id=5, precio_anterior=150.00, precio_nuevo=175.00
SELECT producto_id, precio_anterior, precio_nuevo FROM auditoria_productos;

SELECT '--- PRUEBA 4.2: Actualizar Producto ID 5 (Webcam HD) a 200.00 ---' AS Test;
CALL actualizar_precio_con_auditoria(5, 200.00);

SELECT 'Registro de auditoría (debe tener 2 filas):' AS Check;
-- Debe mostrar el segundo registro: precio_anterior=175.00, precio_nuevo=200.00
SELECT producto_id, precio_anterior, precio_nuevo FROM auditoria_productos;


-- DROP TABLE IF EXISTS productos CASCADE;
-- DROP TABLE IF EXISTS auditoria_productos CASCADE;
