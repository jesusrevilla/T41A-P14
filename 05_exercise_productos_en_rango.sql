CREATE OR REPLACE PROCEDURE productos_en_rango(
    IN p_min NUMERIC,
    IN p_max NUMERIC,
    OUT p_cur REFCURSOR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_min NUMERIC := p_min;
    v_max NUMERIC := p_max;
BEGIN
    IF v_min IS NULL OR v_max IS NULL THEN
        RAISE EXCEPTION 'Los parámetros p_min y p_max no pueden ser NULL';
    END IF;

    IF v_min > v_max THEN
        v_min := p_max;
        v_max := p_min;
    END IF;

    p_cur := 'cur_productos_en_rango';
    OPEN p_cur FOR
        SELECT id, nombre, precio, creado_en
        FROM productos
        WHERE precio BETWEEN v_min AND v_max
        ORDER BY precio;
END;
$$;
