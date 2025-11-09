CREATE TABLE productos(
  id serial,
  nombre text,
  precio numeric(10,2)
);



CREATE TABLE productos_auditoria (
    id_auditoria SERIAL PRIMARY KEY,
    id_producto INT,
    nombre_anterior TEXT,
    precio_anterior NUMERIC(10,2),
    nombre_nuevo TEXT,
    precio_nuevo NUMERIC(10,2),
    usuario_db TEXT DEFAULT current_user,
    fecha_cambio TIMESTAMP DEFAULT now()
);
