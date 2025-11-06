CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    stock INT NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL
);
