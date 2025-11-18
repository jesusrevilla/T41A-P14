

SELECT * FROM productos ORDER BY id;

-- Probar aumento de precios (10%)
CALL increase_product_prices(10);

-- Mostrar productos después del aumento
SELECT * FROM productos ORDER BY id;

-- Probar búsqueda por rango de precios
CALL get_products_in_price_range(100, 500, 0, '');

-- Probar trigger de auditoría
UPDATE productos SET precio = 1500.00 WHERE nombre = 'Laptop Gaming';

-- Mostrar registros de auditoría
SELECT * FROM audit_productos ORDER BY id DESC;
