-- Crea la tabla de auditoría para registrar actualizaciones de precio
CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INT,
    precio_anterior NUMERIC,
    precio_nuevo NUMERIC,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
