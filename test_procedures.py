import pytest
import psycopg2

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def test_increase_prices_procedure():
    conn = get_connection()
    cur = conn.cursor()
    
    # Obtener precio antes del aumento
    cur.execute("SELECT precio FROM productos WHERE nombre = 'Laptop Gaming'")
    precio_original = cur.fetchone()[0]
    
    # Ejecutar procedimiento
    cur.execute("CALL increase_product_prices(10)")
    conn.commit()
    
    # Verificar el aumento
    cur.execute("SELECT precio FROM productos WHERE nombre = 'Laptop Gaming'")
    precio_nuevo = cur.fetchone()[0]
    
    aumento_esperado = precio_original * 1.10
    assert abs(precio_nuevo - aumento_esperado) < 0.01
    
    cur.close()
    conn.close()

def test_products_in_range_procedure():
    conn = get_connection()
    cur = conn.cursor()
    
    # Ejecutar procedimiento
    cur.execute("CALL get_products_in_price_range(100, 500, 0, '')")
    result = cur.fetchone()
    
    product_count = result[0]
    result_message = result[1]
    
    # Verificar que tenemos resultados
    assert product_count >= 0
    assert 'productos' in result_message
    
    cur.close()
    conn.close()

def test_audit_trigger():
    conn = get_connection()
    cur = conn.cursor()
    
    # Actualizar un precio para activar el trigger
    cur.execute("UPDATE productos SET precio = 1300.00 WHERE nombre = 'Laptop Gaming'")
    conn.commit()
    
    # Verificar que se creó registro de auditoría
    cur.execute("SELECT COUNT(*) FROM audit_productos WHERE accion = 'UPDATE'")
    audit_count = cur.fetchone()[0]
    
    assert audit_count >= 1
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
