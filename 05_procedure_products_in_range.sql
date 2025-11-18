
CREATE OR REPLACE PROCEDURE get_products_in_price_range(
    IN min_price NUMERIC,
    IN max_price NUMERIC,
    OUT product_count INTEGER,
    OUT result_message TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
  
    IF min_price > max_price THEN
        RAISE EXCEPTION 'El precio mínimo no puede ser mayor al precio máximo';
    END IF;
    
    
    SELECT COUNT(*) INTO product_count
    FROM productos
    WHERE precio BETWEEN min_price AND max_price;
    
   
    IF product_count > 0 THEN
        result_message := 'Se encontraron ' || product_count || 
                         ' productos en el rango $' || min_price || 
                         ' - $' || max_price;
    ELSE
        result_message := 'No se encontraron productos en el rango $' || 
                         min_price || ' - $' || max_price;
    END IF;
    
    RAISE NOTICE '%', result_message;
END;
$$;
