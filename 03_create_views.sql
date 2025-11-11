CREATE PROCEDURE eliminar_producto(p_id INT)
LANGUAGE plpgsql 
AS $$
DECLARE
    v_nombre TEXT;
BEGIN
    SELECT nombre INTO v_nombre FROM productos WHERE id = p_id;
    IF NOT FOUND THEN
        RAISE NOTICE 'Producto no encontrado';
    ELSE
        DELETE FROM productos WHERE id = p_id;
        RAISE NOTICE 'Producto eliminado';
    END IF;
END;
$$;

CREATE PROCEDURE aumentar_precios(
    p_porcentaje NUMERIC
)
LANGUAGE plpgsql 
AS $$
BEGIN
    UPDATE productos
    SET precio = precio * (1 + (p_porcentaje / 100));
END;
$$;

CREATE  PROCEDURE buscar_por_rango(
    p_minimo NUMERIC,
    p_maximo NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS resultados_productos (
        id INT,
        nombre TEXT,
        precio NUMERIC(10,2)
    ) ON COMMIT DROP;

    TRUNCATE TABLE resultados_productos;

    INSERT INTO resultados_productos
    SELECT *
    FROM productos
    WHERE precio BETWEEN p_minimo AND p_maximo
    ORDER BY precio ASC;

END;
$$;

CREATE OR REPLACE PROCEDURE actualizar_producto(
    p_id INT,
    p_nuevo_nombre TEXT,
    p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql AS $$
DECLARE
    v_anterior RECORD;
BEGIN
    SELECT * INTO v_anterior FROM productos WHERE id = p_id;

    IF NOT FOUND THEN
        RAISE NOTICE 'No se actualizó nada.';
        RETURN;
    END IF;

    UPDATE productos
    SET
        nombre = p_nuevo_nombre,
        precio = p_nuevo_precio
    WHERE id = p_id;

    INSERT INTO productos_auditoria (
        id_producto,
        nombre_anterior,
        precio_anterior,
        nombre_nuevo,
        precio_nuevo
    )
    VALUES (
        p_id,
        v_anterior.nombre,
        v_anterior.precio,
        p_nuevo_nombre,
        p_nuevo_precio 
    );
END;
$$;
