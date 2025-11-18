#!/usr/bin/env python3
"""
Tests simples para los procedimientos almacenados de PostgreSQL
"""

import psycopg2
import sys

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def test_connection():
    """Test de conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        assert result[0] == 1
        print(" Test de conexión: PASS")
        return True
    except Exception as e:
        print(f" Test de conexión: FAIL - {e}")
        return False

def test_increase_prices():
    """Test del procedimiento increase_product_prices"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Obtener precio antes del aumento
        cur.execute("SELECT precio FROM productos WHERE nombre = 'Laptop Gaming'")
        precio_original = cur.fetchone()[0]
        
        # Ejecutar procedimiento (aumento del 10%)
        cur.execute("CALL increase_product_prices(10)")
        conn.commit()
        
        # Verificar el aumento
        cur.execute("SELECT precio FROM productos WHERE nombre = 'Laptop Gaming'")
        precio_nuevo = cur.fetchone()[0]
        
        aumento_esperado = precio_original * 1.10
        diferencia = abs(precio_nuevo - aumento_esperado)
        
        assert diferencia < 0.01, f"Diferencia muy grande: {diferencia}"
        print(f" Test increase_product_prices: PASS")
        print(f"   Precio original: ${precio_original:.2f}")
        print(f"   Precio nuevo: ${precio_nuevo:.2f}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f" Test increase_product_prices: FAIL - {e}")
        return False

def test_products_in_range():
    """Test del procedimiento get_products_in_price_range"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Ejecutar procedimiento
        cur.execute("CALL get_products_in_price_range(100, 500, 0, '')")
        result = cur.fetchone()
        
        product_count = result[0]
        result_message = result[1]
        
        # Verificar que tenemos resultados coherentes
        assert product_count >= 0
        assert 'productos' in result_message
        
        print(f" Test get_products_in_price_range: PASS")
        print(f"   Productos encontrados: {product_count}")
        print(f"   Mensaje: {result_message}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f" Test get_products_in_price_range: FAIL - {e}")
        return False

def test_audit_trigger():
    """Test del trigger de auditoría"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Contar registros de auditoría antes
        cur.execute("SELECT COUNT(*) FROM audit_productos")
        count_antes = cur.fetchone()[0]
        
        # Actualizar un precio para activar el trigger
        cur.execute("UPDATE productos SET precio = 1350.00 WHERE nombre = 'Smartphone'")
        conn.commit()
        
        # Verificar que se creó registro de auditoría
        cur.execute("SELECT COUNT(*) FROM audit_productos")
        count_despues = cur.fetchone()[0]
        
        assert count_despues > count_antes, "No se creó registro de auditoría"
        
        # Mostrar el registro de auditoría
        cur.execute("SELECT * FROM audit_productos ORDER BY id DESC LIMIT 1")
        audit_record = cur.fetchone()
        
        print(f" Test audit_trigger: PASS")
        print(f"   Registros de auditoría: {count_despues}")
        print(f"   Último registro: {audit_record}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f" Test audit_trigger: FAIL - {e}")
        return False

def main():
    """Función principal que ejecuta todos los tests"""
    print(" Iniciando tests de procedimientos PostgreSQL...\n")
    
    tests = [
        test_connection,
        test_increase_prices,
        test_products_in_range,
        test_audit_trigger
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
        print()
    
    print("=" * 50)
    print(f" RESULTADOS:")
    print(f"    PASS: {passed}")
    print(f"    FAIL: {failed}")
    print(f"   TOTAL: {passed + failed}")
    
    if failed == 0:
        print("¡Todos los tests pasaron!")
        sys.exit(0)
    else:
        print(" Algunos tests fallaron")
        sys.exit(1)

if __name__ == '__main__':
    main()
