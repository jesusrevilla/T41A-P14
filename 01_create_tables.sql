-- Catálogo de productos disponibles
CREATE TABLE catalogo_productos (
    producto_id SERIAL PRIMARY KEY,
    nombre_producto TEXT NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL
);

-- Registro de acciones sobre productos
CREATE TABLE log_acciones_productos (
    log_id SERIAL PRIMARY KEY,
    producto_id INT NOT NULL,
    tipo_accion TEXT NOT NULL,
    fecha_accion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
