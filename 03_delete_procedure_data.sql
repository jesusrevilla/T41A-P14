
DROP PROCEDURE IF EXISTS increase_product_prices;
DROP PROCEDURE IF EXISTS get_products_in_price_range;
DROP PROCEDURE IF EXISTS audit_product_updates;


TRUNCATE TABLE audit_productos RESTART IDENTITY;
DELETE FROM productos;

ALTER SEQUENCE productos_id_seq RESTART WITH 1;
ALTER SEQUENCE audit_productos_id_seq RESTART WITH 1;
