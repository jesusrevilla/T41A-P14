
CREATE OR REPLACE PROCEDURE increase_product_prices(
    IN percentage NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    affected_rows INTEGER;
BEGIN
    
    IF percentage <= 0 THEN
        RAISE EXCEPTION 'El porcentaje debe ser mayor que cero';
    END IF;
    
    
    UPDATE productos 
    SET precio = precio * (1 + percentage/100);
    
    GET DIAGNOSTICS affected_rows = ROW_COUNT;
    
   
    RAISE NOTICE 'Se actualizaron % productos con un aumento del %%%', 
                 affected_rows, percentage;
END;
$$;
