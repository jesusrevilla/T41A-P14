
  CREATE TABLE productos(
  id SERIAL,
  nombre TEXT,
  precio NUMERIC(10,2)
  );

CREATE TABLE IF NOT EXISTS productos_auditoria (
    id_auditoria SERIAL PRIMARY KEY,
    id_producto INT,
    nombre_anterior TEXT,
    precio_anterior NUMERIC(10,2),
    nombre_nuevo TEXT,
    precio_nuevo NUMERIC(10,2),
    usuario_db TEXT DEFAULT current_user,
    fecha_cambio TIMESTAMP DEFAULT now()
);
