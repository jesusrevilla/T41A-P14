-- 01_create_table.sql
-- Crear las tablas de productos y auditoría de productos

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio NUMERIC(10,2),
    stock INT
);

CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INT,
    accion VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 02_insert_data.sql
-- Insertar datos de ejemplo en la tabla productos

INSERT INTO productos (nombre, precio, stock) VALUES
('Laptop', 15000.00, 10),
('Mouse', 250.00, 50),
('Teclado', 450.00, 30),
('Monitor', 3000.00, 15),
('USB', 120.00, 100);


-- 03_eliminar_producto.sql
-- Crear procedimiento para eliminar un producto por ID

CREATE OR REPLACE PROCEDURE eliminar_producto(producto_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    existe BOOLEAN;
BEGIN
    SELECT EXISTS(SELECT 1 FROM productos WHERE id = producto_id) INTO existe;

    IF existe THEN
        DELETE FROM productos WHERE id = producto_id;
        -- Registrar la eliminación en auditoría (opcional)
        INSERT INTO auditoria_productos (producto_id, accion)
        VALUES (producto_id, 'Eliminación');
        RAISE NOTICE 'Producto con ID % eliminado exitosamente.', producto_id;
    ELSE
        RAISE NOTICE 'No se encontró ningún producto con el ID %. No se realizó ninguna eliminación.', producto_id;
    END IF;
END;
$$;


-- 04_aumentar_precios.sql
-- Crear procedimiento para aumentar los precios de los productos

CREATE OR REPLACE PROCEDURE aumentar_precios(porcentaje NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos
    SET precio = precio + (precio * (porcentaje / 100));

    -- Registrar el aumento de precios en auditoría (opcional)
    INSERT INTO auditoria_productos (producto_id, accion)
    SELECT id, 'Aumento de precio'
    FROM productos;

    RAISE NOTICE 'Se han aumentado los precios en un % porcentaje.', porcentaje;
END;
$$;


-- 05_obtener_productos_rango.sql
-- Crear función para obtener productos dentro de un rango de precios

CREATE OR REPLACE FUNCTION obtener_productos_rango(precio_min NUMERIC, precio_max NUMERIC)
RETURNS TABLE(id INT, nombre VARCHAR, precio NUMERIC, stock INT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, nombre, precio, stock
    FROM productos
    WHERE precio BETWEEN precio_min AND precio_max
    ORDER BY precio ASC;
END;
$$ LANGUAGE plpgsql;
