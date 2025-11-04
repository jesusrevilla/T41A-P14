-- 1. Procedimiento que elimina un producto por su ID y devuelve mensaje
CREATE OR REPLACE PROCEDURE eliminar_producto(
    IN p_id INT,
    OUT p_mensaje TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_nombre_producto TEXT;
BEGIN
    -- Verificar si el producto existe
    SELECT nombre INTO v_nombre_producto
    FROM productos 
    WHERE id = p_id;
    
    IF FOUND THEN
        -- Eliminar el producto
        DELETE FROM productos WHERE id = p_id;
        p_mensaje := 'Producto "' || v_nombre_producto || '" eliminado exitosamente.';
        RAISE NOTICE 'Eliminación exitosa: %', p_mensaje;
    ELSE
        p_mensaje := 'Error: No se encontró el producto con ID ' || p_id;
        RAISE NOTICE 'Error en eliminación: %', p_mensaje;
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        p_mensaje := 'Error inesperado: ' || SQLERRM;
        RAISE NOTICE 'Excepción: %', p_mensaje;
END;
$$;

-- 2. Procedimiento que aumenta el precio de todos los productos en un porcentaje dado
CREATE OR REPLACE PROCEDURE aumentar_precios_porcentaje(
    IN p_porcentaje NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contador INT := 0;
    v_producto RECORD;
BEGIN
    -- Validar que el porcentaje sea positivo
    IF p_porcentaje <= 0 THEN
        RAISE NOTICE 'El porcentaje debe ser mayor que cero.';
        RETURN;
    END IF;
    
    -- Mostrar precios antes del aumento
    RAISE NOTICE 'Precios antes del aumento:';
    FOR v_producto IN SELECT nombre, precio FROM productos LOOP
        RAISE NOTICE '- %: %', v_producto.nombre, v_producto.precio;
    END LOOP;
    
    -- Actualizar precios
    UPDATE productos 
    SET precio = precio * (1 + p_porcentaje/100);
    
    -- Contar productos afectados
    GET DIAGNOSTICS v_contador = ROW_COUNT;
    
    -- Mostrar precios después del aumento
    RAISE NOTICE 'Precios después del aumento (%):', p_porcentaje;
    FOR v_producto IN SELECT nombre, precio FROM productos LOOP
        RAISE NOTICE '- %: %', v_producto.nombre, v_producto.precio;
    END LOOP;
    
    RAISE NOTICE 'Total de productos actualizados: %', v_contador;
END;
$$;

-- 3. Procedimiento que devuelve productos dentro de un rango de precios
CREATE OR REPLACE PROCEDURE obtener_productos_por_rango_precio(
    IN p_precio_min NUMERIC,
    IN p_precio_max NUMERIC,
    INOUT p_resultados REFCURSOR DEFAULT 'productos_cursor'
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validar rango de precios
    IF p_precio_min > p_precio_max THEN
        RAISE NOTICE 'Error: El precio mínimo no puede ser mayor al precio máximo.';
        RETURN;
    END IF;
    
    IF p_precio_min < 0 OR p_precio_max < 0 THEN
        RAISE NOTICE 'Error: Los precios no pueden ser negativos.';
        RETURN;
    END IF;
    
    -- Abrir cursor con los resultados
    OPEN p_resultados FOR
    SELECT id, nombre, precio, fecha_creacion
    FROM productos
    WHERE precio BETWEEN p_precio_min AND p_precio_max
    ORDER BY precio;
    
    RAISE NOTICE 'Búsqueda completada. Use FETCH ALL FROM "%" para ver los resultados.', p_resultados;
END;
$$;

-- 4. Procedimiento para actualizar producto con auditoría
CREATE OR REPLACE PROCEDURE actualizar_producto_con_auditoria(
    IN p_id INT,
    IN p_nuevo_nombre TEXT,
    IN p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_precio_anterior NUMERIC;
    v_nombre_anterior TEXT;
BEGIN
    -- Obtener valores actuales
    SELECT precio, nombre INTO v_precio_anterior, v_nombre_anterior
    FROM productos 
    WHERE id = p_id;
    
    IF NOT FOUND THEN
        RAISE NOTICE 'Error: No se encontró el producto con ID %', p_id;
        RETURN;
    END IF;
    
    -- Validar nuevo precio
    IF p_nuevo_precio <= 0 THEN
        RAISE NOTICE 'Error: El precio debe ser mayor que cero.';
        RETURN;
    END IF;
    
    -- Iniciar transacción
    BEGIN
        -- Actualizar producto
        UPDATE productos 
        SET nombre = p_nuevo_nombre,
            precio = p_nuevo_precio
        WHERE id = p_id;
        
        -- Registrar en auditoría si el precio cambió
        IF v_precio_anterior != p_nuevo_precio THEN
            INSERT INTO auditoria_productos (producto_id, precio_anterior, precio_nuevo)
            VALUES (p_id, v_precio_anterior, p_nuevo_precio);
            
            RAISE NOTICE 'Auditoría: Precio cambiado de % a %', v_precio_anterior, p_nuevo_precio;
        END IF;
        
        RAISE NOTICE 'Producto actualizado exitosamente.';
        
        -- Confirmar transacción
        COMMIT;
        
    EXCEPTION
        WHEN OTHERS THEN
            -- Revertir en caso de error
            ROLLBACK;
            RAISE NOTICE 'Error en la actualización: %', SQLERRM;
    END;
END;
$$;
