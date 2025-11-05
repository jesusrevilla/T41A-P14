CREATE PROCEDURE eliminar_producto(
    p_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM productos
    WHERE id = p_id;

    IF FOUND THEN
        RAISE NOTICE 'Producto eliminado exitosamente (ID: %)', p_id;
    ELSE
        RAISE NOTICE 'Error: No se encontró un producto con el ID %.', p_id;
    END IF;
END;
$$;



CREATE PROCEDURE aumentar_precios(
    p_porcentaje DECIMAL(5, 2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    filas_afectadas INT; 
BEGIN
    IF p_porcentaje < 0 THEN
        RAISE EXCEPTION 'El porcentaje de aumento no puede ser negativo.';
    END IF;
    UPDATE productos
    SET precio = precio * (1 + (p_porcentaje / 100));

    GET DIAGNOSTICS filas_afectadas = ROW_COUNT;
    
    RAISE NOTICE 'Precios actualizados. % filas afectadas.', filas_afectadas;
    
END;
$$;


CREATE PROCEDURE buscar_por_rango(
    p_minimo DECIMAL(10, 2),
    p_maximo DECIMAL(10, 2)
)
LANGUAGE plpgsql
AS $$
DECLARE

    v_producto RECORD;
BEGIN
    IF p_minimo > p_maximo THEN
        RAISE EXCEPTION 'El precio mínimo (%) no puede ser mayor que el máximo (%).', p_minimo, p_maximo;
    END IF;

    RAISE NOTICE '--- Productos encontrados (Rango: % a %) ---', p_minimo, p_maximo;

    FOR v_producto IN
        SELECT *
        FROM productos
        WHERE precio BETWEEN p_minimo AND p_maximo
        ORDER BY precio
    LOOP

        RAISE NOTICE 'ID: %, Nombre: %, Precio: $%', 
                     v_producto.id, v_producto.nombre, v_producto.precio;
    END LOOP;
    
    RAISE NOTICE 'Fin de la búsqueda';
END;
$$;

