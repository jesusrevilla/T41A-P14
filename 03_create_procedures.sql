
-- 1. Procedimiento para eliminar producto por ID
CREATE OR REPLACE PROCEDURE eliminar_producto(IN p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM productos WHERE id = p_id) THEN
        DELETE FROM productos WHERE id = p_id;
        RAISE NOTICE 'Producto con ID % eliminado.', p_id;
    ELSE
        RAISE NOTICE 'No se encontró producto con ID %.', p_id;
    END IF;
END;
$$;



-- 2. Procedimiento para aumentar precios en un porcentaje
CREATE OR REPLACE PROCEDURE aumentar_precios(IN p_porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET precio = precio * (1 + p_porcentaje / 100);
    
    -- Mostrar el porcentaje aplicado correctamente
    RAISE NOTICE 'Precios aumentados en % por ciento.', p_porcentaje;
END;
$$;



-- 3. Procedimiento para mostrar productos en un rango de precios
CREATE OR REPLACE PROCEDURE productos_en_rango(IN p_min NUMERIC, IN p_max NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    prod RECORD;
BEGIN
    FOR prod IN SELECT * FROM productos WHERE precio BETWEEN p_min AND p_max LOOP
        RAISE NOTICE 'ID: %, Nombre: %, Precio: %', prod.id, prod.nombre, prod.precio;
    END LOOP;
END;
$$;



-- 4. Procedimiento para actualizar precio y registrar en auditoría
CREATE OR REPLACE PROCEDURE actualizar_precio_auditado(IN p_id INT, IN p_nuevo_precio NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    v_precio_anterior NUMERIC;
BEGIN
    SELECT precio INTO v_precio_anterior FROM productos WHERE id = p_id;

    IF FOUND THEN
        UPDATE productos SET precio = p_nuevo_precio WHERE id = p_id;

        INSERT INTO auditoria_productos (producto_id, precio_anterior, precio_nuevo)
        VALUES (p_id, v_precio_anterior, p_nuevo_precio);

        RAISE NOTICE 'Precio actualizado y registrado en auditoría.';
    ELSE
        RAISE NOTICE 'Producto no encontrado.';
    END IF;
END;
$$;
