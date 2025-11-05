CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  precio NUMERIC NOT NULL
);

CREATE TABLE auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INT NOT NULL,
    precio_anterior NUMERIC,
    precio_nuevo NUMERIC
);
