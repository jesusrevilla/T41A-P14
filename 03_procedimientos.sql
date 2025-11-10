-- Elimina un producto por id
CREATE OR REPLACE PROCEDURE borrar_producto(IN producto_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM catalogo_productos WHERE producto_id = producto_id;

    IF FOUND THEN
        RAISE NOTICE 'Producto eliminado: ID %', producto_id;
    ELSE
        RAISE NOTICE 'Producto no encontrado: ID %', producto_id;
    END IF;
END;
$$;

-- Aumenta precios por porcentaje
CREATE OR REPLACE PROCEDURE ajustar_precios(IN porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    item RECORD;
    factor NUMERIC := 1 + (porcentaje / 100);
BEGIN
    IF porcentaje <= 0 THEN
        RAISE NOTICE 'Debe ser mayor que cero.';
        RETURN;
    END IF;

    FOR item IN SELECT producto_id, nombre_producto, precio_unitario FROM catalogo_productos LOOP
        UPDATE catalogo_productos
        SET precio_unitario = precio_unitario * factor
        WHERE producto_id = item.producto_id;

        RAISE NOTICE 'Porcentaje actualizado, el nuevo precio es: %',
            item.nombre_producto, item.precio_unitario * factor;
    END LOOP;

    RAISE NOTICE 'Ajuste completado';
END;
$$;

-- Muestra productos dentro de un rango
CREATE OR REPLACE PROCEDURE listar_productos_por_precio(IN minimo NUMERIC, IN maximo NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    item RECORD;
BEGIN
    IF minimo > maximo THEN
        RAISE NOTICE 'Mínimo no puede ser mayor que máximo.';
        RETURN;
    END IF;

    FOR item IN SELECT producto_id, nombre_producto, precio_unitario
                FROM catalogo_productos
                WHERE precio_unitario BETWEEN minimo AND maximo
                ORDER BY precio_unitario LOOP
        RAISE NOTICE 'ID: %, Nombre: %, Precio: %',
            item.producto_id, item.nombre_producto, item.precio_unitario;
    END LOOP;

    RAISE NOTICE 'fin';
END;
$$;
