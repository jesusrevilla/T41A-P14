# T41A-P14

# Procedimientos Almacenados en PostgreSQL

## 📘 Introducción
Los **procedimientos almacenados** en PostgreSQL permiten encapsular lógica de negocio dentro de la base de datos, facilitando la reutilización de código, mejorando el rendimiento y asegurando la integridad de los datos.

---

## 🧩 Diferencias entre Funciones y Procedimientos

| Característica         | Funciones (`FUNCTION`) | Procedimientos (`PROCEDURE`) |
|------------------------|-------------------------|-------------------------------|
| Devuelven valor        | Sí                      | No necesariamente             |
| Uso en SELECT          | Sí                      | No                            |
| Invocación             | `SELECT` o `CALL`       | `CALL`                        |
| Parámetros OUT         | Sí                      | Sí                            |

---

## 🛠️ Sintaxis Básica

```sql
CREATE PROCEDURE nombre_procedimiento(param1 tipo, param2 tipo)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Instrucciones SQL
END;
$$;
```

---

## 🧪 Ejemplo 1: Insertar un Producto

```sql
CREATE PROCEDURE insertar_producto(nombre TEXT, precio NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO productos(nombre, precio)
    VALUES (nombre, precio);
END;
$$;
```

**Llamada:**
```sql
CALL insertar_producto('Teclado', 299.99);
```

---

## 🔁 Ejemplo 2: Procedimiento con Parámetros de Salida

```sql
CREATE PROCEDURE obtener_precio_producto(
    IN p_nombre TEXT,
    OUT p_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT precio INTO p_precio
    FROM productos
    WHERE nombre = p_nombre;
END;
$$;
```

**Llamada:**
```sql
CALL obtener_precio_producto('Teclado', NULL);
```

---

## 🔄 Ejemplo 3: Control de Flujo

```sql
CREATE PROCEDURE actualizar_precio(
    IN p_id INT,
    IN p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_nuevo_precio > 0 THEN
        UPDATE productos
        SET precio = p_nuevo_precio
        WHERE id = p_id;
    ELSE
        RAISE NOTICE 'El precio debe ser mayor que cero.';
    END IF;
END;
$$;
```

---

## 🧠 Ejercicios Propuestos

1. Crear un procedimiento que elimine un producto por su ID y devuelva un mensaje indicando si fue exitoso o no.
2. Crear un procedimiento que recorra todos los productos y aumente su precio en un porcentaje dado.
3. Crear un procedimiento que reciba un rango de precios y devuelva los productos dentro de ese rango.
4. Modificar un procedimiento para registrar en una tabla de auditoría cada vez que se actualiza un producto.

---

## ✅ Recomendaciones
- Utiliza `RAISE NOTICE` para depurar procedimientos.
- Usa transacciones (`BEGIN`, `COMMIT`, `ROLLBACK`) si el procedimiento realiza varias operaciones críticas.
- Documenta cada procedimiento con comentarios claros.

---

## 📚 Recursos Adicionales
- [Documentación oficial de PostgreSQL sobre procedimientos](https://www.postgresql.org/docs/current/sql-createprocedure.html)
- Tutoriales en [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

---
