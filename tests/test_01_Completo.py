\echo '=== INICIANDO TESTS COMPLETOS ==='

-- =============================================
-- TEST 1: Procedimiento eliminar_producto
-- =============================================
\echo ''
\echo '🧪 TEST 1: Eliminar Producto'

-- Test 1.1: Eliminar producto existente
\echo 'Test 1.1: Eliminar producto existente (ID 1)'
DO $$
DECLARE
    mensaje TEXT;
BEGIN
    CALL eliminar_producto(1, mensaje);
    RAISE NOTICE 'Resultado: %', mensaje;
END $$;

-- Test 1.2: Intentar eliminar producto inexistente
\echo 'Test 1.2: Intentar eliminar producto inexistente (ID 999)'
DO $$
DECLARE
    mensaje TEXT;
BEGIN
    CALL eliminar_producto(999, mensaje);
    RAISE NOTICE 'Resultado: %', mensaje;
END $$;

-- Verificar estado después de las eliminaciones
\echo 'Estado de productos después de TEST 1:'
SELECT id, nombre, precio FROM productos ORDER BY id;

-- =============================================
-- TEST 2: Procedimiento aumentar_precios_porcentaje
-- =============================================
\echo ''
\echo '🧪 TEST 2: Aumentar Precios'

-- Test 2.1: Aumento del 10%
\echo 'Test 2.1: Aumento del 10%'
CALL aumentar_precios_porcentaje(10);

-- Test 2.2: Intentar aumento con porcentaje negativo
\echo 'Test 2.2: Intentar aumento con porcentaje negativo (-5%)'
CALL aumentar_precios_porcentaje(-5);

-- Test 2.3: Aumento del 5%
\echo 'Test 2.3: Aumento del 5%'
CALL aumentar_precios_porcentaje(5);

-- Verificar precios después del TEST 2
\echo 'Precios después de TEST 2:'
SELECT nombre, precio FROM productos ORDER BY precio;

-- =============================================
-- TEST 3: Procedimiento obtener_productos_por_rango_precio
-- =============================================
\echo ''
\echo '🧪 TEST 3: Rango de Precios'

-- Test 3.1: Rango válido (150 - 2000)
\echo 'Test 3.1: Rango válido (150 - 2000)'
DO $$
DECLARE
    cur REFCURSOR;
    producto_record RECORD;
    contador INT := 0;
BEGIN
    CALL obtener_productos_por_rango_precio(150, 2000, cur);
    
    RAISE NOTICE 'Productos en el rango 150-2000:';
    LOOP
        FETCH cur INTO producto_record;
        EXIT WHEN NOT FOUND;
        contador := contador + 1;
        RAISE NOTICE '- %: % (Precio: %)', producto_record.id, producto_record.nombre, producto_record.precio;
    END LOOP;
    
    IF contador = 0 THEN
        RAISE NOTICE 'No se encontraron productos en este rango.';
    ELSE
        RAISE NOTICE 'Total encontrados: %', contador;
    END IF;
    
    CLOSE cur;
END $$;

-- Test 3.2: Rango inválido (mínimo > máximo)
\echo 'Test 3.2: Rango inválido (1000 > 100)'
DO $$
DECLARE
    cur REFCURSOR;
BEGIN
    CALL obtener_productos_por_rango_precio(1000, 100, cur);
END $$;

-- Test 3.3: Rango con precios negativos
\echo 'Test 3.3: Rango con precios negativos'
DO $$
DECLARE
    cur REFCURSOR;
BEGIN
    CALL obtener_productos_por_rango_precio(-100, 500, cur);
END $$;

-- =============================================
-- TEST 4: Procedimiento actualizar_producto_con_auditoria
-- =============================================
\echo ''
\echo '🧪 TEST 4: Auditoría de Productos'

-- Verificar estado inicial antes del TEST 4
\echo 'Estado inicial antes de TEST 4:'
SELECT id, nombre, precio FROM productos ORDER BY id;

\echo 'Registros de auditoría antes de TEST 4:'
SELECT * FROM auditoria_productos ORDER BY fecha_cambio;

-- Test 4.1: Actualización exitosa con cambio de precio
\echo 'Test 4.1: Actualización con cambio de precio (ID 2)'
CALL actualizar_producto_con_auditoria(2, 'Mouse Gamer Pro', 250.00);

-- Test 4.2: Actualización con precio inválido
\echo 'Test 4.2: Actualización con precio inválido (ID 3)'
CALL actualizar_producto_con_auditoria(3, 'Monitor', -500.00);

-- Test 4.3: Actualización de producto inexistente
\echo 'Test 4.3: Actualización de producto inexistente (ID 999)'
CALL actualizar_producto_con_auditoria(999, 'Producto Fake', 100.00);

-- Test 4.4: Actualización solo de nombre (mismo precio)
\echo 'Test 4.4: Actualización solo de nombre (mismo precio - ID 4)'
CALL actualizar_producto_con_auditoria(4, 'CPU Gamer', 2500.75);

-- Verificar estado final del TEST 4
\echo 'Estado final después de TEST 4:'
SELECT id, nombre, precio FROM productos ORDER BY id;

\echo 'Registros de auditoría generados en TEST 4:'
SELECT * FROM auditoria_productos ORDER BY fecha_cambio;

-- =============================================
-- TEST 5: Pruebas adicionales y casos edge
-- =============================================
\echo ''
\echo '🧪 TEST 5: Pruebas Adicionales'

-- Test 5.1: Aumento del 0% (no debería cambiar nada)
\echo 'Test 5.1: Aumento del 0%'
CALL aumentar_precios_porcentaje(0);

-- Test 5.2: Rango extremo (precios muy altos)
\echo 'Test 5.2: Rango extremo (5000 - 10000)'
DO $$
DECLARE
    cur REFCURSOR;
    producto_record RECORD;
    contador INT := 0;
BEGIN
    CALL obtener_productos_por_rango_precio(5000, 10000, cur);
    
    RAISE NOTICE 'Productos en rango 5000-10000:';
    LOOP
        FETCH cur INTO producto_record;
        EXIT WHEN NOT FOUND;
        contador := contador + 1;
        RAISE NOTICE '- %', producto_record.nombre;
    END LOOP;
    
    IF contador = 0 THEN
        RAISE NOTICE 'No hay productos en este rango (esperado).';
    END IF;
    
    CLOSE cur;
END $$;

-- =============================================
-- RESUMEN FINAL
-- =============================================
\echo ''
\echo '=== RESUMEN FINAL ==='

\echo 'Productos finales en la base de datos:'
SELECT 
    id,
    nombre,
    precio,
    CASE 
        WHEN precio > 2000 THEN 'ALTO'
        WHEN precio > 500 THEN 'MEDIO'
        ELSE 'BAJO'
    END as categoria_precio
FROM productos 
ORDER BY precio DESC;

\echo 'Total de registros de auditoría:'
SELECT 
    COUNT(*) as total_auditorias,
    COUNT(DISTINCT producto_id) as productos_auditados
FROM auditoria_productos;

\echo 'Resumen de cambios de precio auditados:'
SELECT 
    producto_id,
    COUNT(*) as cambios,
    MIN(precio_anterior) as precio_min_anterior,
    MAX(precio_nuevo) as precio_max_nuevo
FROM auditoria_productos 
GROUP BY producto_id 
ORDER BY producto_id;

\echo '=== TODOS LOS TESTS COMPLETADOS ==='
