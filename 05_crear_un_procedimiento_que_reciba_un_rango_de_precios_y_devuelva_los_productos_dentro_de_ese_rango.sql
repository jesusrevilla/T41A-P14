CREATE PROCEDURE productos_en_rango(
    IN p_min NUMERIC,
    IN p_max NUMERIC,
    OUT p_resultados REFCURSOR
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN p_resultados FOR
        SELECT * FROM productos
        WHERE precio BETWEEN p_min AND p_max;
END;
$$;

-- Ejemplo de llamada:
CALL productos_en_rango(100, 1000, 'cur');
FETCH ALL FROM cur;
