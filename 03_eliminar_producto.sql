CREATE OR REPLACE PROCEDURE eliminar_producto(IN p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos
    WHERE id = p_id;

    IF FOUND THEN
        RAISE NOTICE 'Producto eliminado correctamente.';
    ELSE
        RAISE NOTICE 'No se encontró el producto';
    END IF;
END;
$$;


CALL eliminar_producto(3);




CREATE OR REPLACE PROCEDURE productos_por_rango(
    IN p_min NUMERIC,
    IN p_max NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    IF p_min > p_max THEN
        RAISE NOTICE 'El precio mínimo no puede ser mayor que el máximo.';
        RETURN;
    END IF;

    FOR r IN
        SELECT id, nombre, precio
        FROM productos
        WHERE precio BETWEEN p_min AND p_max
        ORDER BY precio
    LOOP
        RAISE NOTICE 'ID: %, Nombre: %, Precio: %', r.id, r.nombre, r.precio;
    END LOOP;

    IF NOT FOUND THEN
        RAISE NOTICE 'No se encontraron productos en el rango %.2f - %.2f', p_min, p_max;
    ELSE
        RAISE NOTICE 'Fin de listado.';
    END IF;
END;
$$;

CALL productos_por_rango(50, 200);
