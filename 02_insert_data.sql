INSERT INTO productos (nombre, precio) VALUES
  ('Teclado', 299.99),
  ('Mouse', 199.90),
  ('Monitor', 3500.00),
  ('Silla', 2000.00),
  ('USB-C Hub', 850.00)
ON CONFLICT (nombre) DO NOTHING;