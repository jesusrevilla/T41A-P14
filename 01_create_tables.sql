CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    stock INT NOT NULL,
    precio NUMERIC(10,2) NOT NULL
);
