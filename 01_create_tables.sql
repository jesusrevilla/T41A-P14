CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    precio NUMERIC(12,2) NOT NULL CHECK (precio >= 0),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE auditoria_precios (
    id BIGSERIAL PRIMARY KEY,
    producto_id INT NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    precio_anterior NUMERIC(12,2) NOT NULL,
    precio_nuevo NUMERIC(12,2) NOT NULL,
    cambiado_por TEXT NOT NULL DEFAULT CURRENT_USER,
    motivo TEXT,
    cambiado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
