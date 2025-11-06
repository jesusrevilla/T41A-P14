DROP TABLE IF EXISTS productos;

-- Crea la tabla
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    precio NUMERIC(10, 2)
);
