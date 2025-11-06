CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC(10,2) NOT NULL
);

CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INT NOT NULL,
    accion TEXT NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

