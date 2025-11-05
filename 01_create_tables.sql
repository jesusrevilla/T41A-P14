CREATE TABLE productos(
  id SERIAL PRIMARY KEY,
  nombre TEXT,
  precio NUMERIC
);

CREATE TABLE auditoria(
  id SERIAL PRIMARY KEY,
  tabla TEXT,
  tiempo_mod TIMESTAMP
);
