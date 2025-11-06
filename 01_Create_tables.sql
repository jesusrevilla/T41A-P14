DROP TABLE IF EXISTS auditoria_precios;
DROP TABLE IF EXISTS productos;

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC(10,2) NOT NULL
);

CREATE TABLE auditoria_precios (
    id SERIAL PRIMARY KEY,
    id_producto INT,
    precio_anterior NUMERIC(10,2),
    precio_nuevo NUMERIC(10,2),
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
