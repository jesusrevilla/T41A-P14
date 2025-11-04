
-- Crear la tabla de productos si no existe

DROP TABLE IF EXISTS productos CASCADE;

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC NOT NULL
);


-- DATOS DE PRUEBA

INSERT INTO productos (nombre, precio) VALUES
('Laptop Pro', 1200.00),
('Mouse Ergonomico', 35.50),
('Monitor 4K', 450.00),
('Teclado Mecanico', 80.00);

SELECT '--- TABLA INICIAL ---' AS Test;
SELECT * FROM productos ORDER BY id;



-- PRUEBAS EJERCICIO 1: eliminar_producto

SELECT '--- PRUEBA 1.1: Eliminar Producto Existente (ID 3) ---' AS Test;
DO $$
DECLARE
    v_mensaje TEXT;
BEGIN
    CALL eliminar_producto(3, v_mensaje);
    RAISE NOTICE 'Resultado: %', v_mensaje;
END $$;

SELECT 'Producto ID 3 debe haber desaparecido:' AS Check;
SELECT * FROM productos WHERE id = 3; -- Debe devolver 0 filas

SELECT '--- PRUEBA 1.2: Intentar Eliminar Producto Inexistente (ID 99) ---' AS Test;
DO $$
DECLARE
    v_mensaje TEXT;
BEGIN
    CALL eliminar_producto(99, v_mensaje);
    RAISE NOTICE 'Resultado: %', v_mensaje;
END $$;
-- No debe haber cambios en la tabla


-- PRUEBAS EJERCICIO 2: aumentar_precio_por_porcentaje

SELECT '--- PRUEBA 2.1: Aumentar Precio en 10% ---' AS Test;
SELECT 'Precios antes del aumento:' AS Check;
SELECT nombre, precio FROM productos ORDER BY id;

CALL aumentar_precio_por_porcentaje(10.0);

SELECT 'Precios después del aumento del 10%:' AS Check;
-- Laptop Pro (1200.00 * 1.10) = 1320.00
-- Mouse Ergonomico (35.50 * 1.10) = 39.05
-- Teclado Mecanico (80.00 * 1.10) = 88.00
SELECT id, nombre, precio FROM productos ORDER BY id;

SELECT '--- PRUEBA 2.2: Intentar con porcentaje inválido ---' AS Test;
-- Debe generar una excepción (falla)
-- CALL aumentar_precio_por_porcentaje(0); -- Descomentar para probar la falla

-- LIMPIEZA

DROP TABLE IF EXISTS productos CASCADE;
-- DROP PROCEDURE IF EXISTS eliminar_producto(INT, TEXT);
-- DROP PROCEDURE IF EXISTS aumentar_precio_por_porcentaje(NUMERIC);
