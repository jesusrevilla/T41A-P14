DROP TABLE IF EXISTS productos CASCADE;

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio >= 0)
);


CREATE OR REPLACE PROCEDURE eliminar_producto(p_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos WHERE id = p_id;
END;
$$;



CREATE OR REPLACE PROCEDURE actualizar_precio_por_porcentaje(p_porcentaje INT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET precio = precio + (precio * p_porcentaje / 100.0);
END;
$$;



CREATE OR REPLACE PROCEDURE sp_mostrar_productos_por_rango(p_min NUMERIC, p_max NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT nombre, precio FROM productos
        WHERE precio BETWEEN p_min AND p_max
    LOOP
        RAISE NOTICE 'Producto: %, Precio: %', r.nombre, r.precio;
    END LOOP;
END;
$$;
