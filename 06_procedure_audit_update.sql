
CREATE OR REPLACE PROCEDURE audit_product_updates()
LANGUAGE plpgsql
AS $$
BEGIN
   
    
    RAISE NOTICE 'Auditoría: Verificando cambios en productos...';
    
    
    IF EXISTS (SELECT 1 FROM audit_productos LIMIT 1) THEN
        RAISE NOTICE 'Se encontraron registros de auditoría';
    ELSE
        RAISE NOTICE 'No hay registros de auditoría recientes';
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION log_product_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND OLD.precio != NEW.precio THEN
        INSERT INTO audit_productos (producto_id, accion, precio_anterior, precio_nuevo)
        VALUES (OLD.id, 'UPDATE', OLD.precio, NEW.precio);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_productos (producto_id, accion, precio_anterior)
        VALUES (OLD.id, 'DELETE', OLD.precio);
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS product_audit_trigger ON productos;
CREATE TRIGGER product_audit_trigger
    AFTER UPDATE OR DELETE ON productos
    FOR EACH ROW
    EXECUTE FUNCTION log_product_changes();
