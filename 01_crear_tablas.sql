-- Crear tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC NOT NULL
);

-- Crear tabla de auditoría
CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INT,
    precio_anterior NUMERIC,
    precio_nuevo NUMERIC,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
