CREATE TABLE productos(
  id SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  precio FLOAT NOT NULL
);

CREATE TABLE auditoria(
  id SERIAL PRIMARY KEY,
  tabla TEXT,
  tiempo_mod TIMESTAMP
);
