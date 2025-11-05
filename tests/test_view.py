import psycopg2
import pytest
from pathlib import Path

# Configura tu base de datos
DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    yield conn
    conn.close()

def run_script(conn, sql_file):
    sql_path = Path(sql_file)
    with open(sql_path, "r", encoding="utf-8") as file:
        script = file.read()
    with conn.cursor() as cur:
        cur.execute(script)
        try:
            result = cur.fetchall()
        except psycopg2.ProgrammingError:
            result = []
        return result

def test_eliminar_producto(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("INSERT INTO productos(nombre, precio) VALUES ('Borrame', 99.9) RETURNING id;")
        pid = cur.fetchone()[0]
        db_connection.commit()

    result = run_script(db_connection, "PROCEDURE_1.sql")

    with db_connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos WHERE id = %s;", (pid,))
        count = cur.fetchone()[0]
    assert count == 0, f"El producto con id {pid} no fue eliminado correctamente"

def test_porcentaje_precio(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("DELETE FROM productos;")
        cur.execute("INSERT INTO productos(nombre, precio) VALUES ('Mouse', 100), ('Teclado', 200);")
        db_connection.commit()

    result = run_script(db_connection, "PROCEDURE_2.sql")

    with db_connection.cursor() as cur:
        cur.execute("SELECT nombre, precio FROM productos ORDER BY nombre;")
        data = cur.fetchall()
    precios = {nombre: precio for nombre, precio in data}
    
    assert round(precios["Mouse"], 1) == 110.0
    assert round(precios["Teclado"], 1) == 220.0
    
def test_rango_precio_notice(db_connection):
    run_script(db_connection, "PROCEDURE_3.sql") 

    cur = db_connection.cursor()
    cur.execute("DELETE FROM productos;")
    cur.execute("""
        INSERT INTO productos (nombre, precio) VALUES
        ('Monitor', 150.00),
        ('Teclado', 50.00),
        ('Mouse', 30.00),
        ('Impresora', 300.00),
        ('Laptop', 800.00);
    """)
    db_connection.commit()
    db_connection.notices.clear()

    cur.execute("CALL rango_precio(100, 400);")
    db_connection.commit()

    notices = db_connection.notices

    for n in notices:
        print("NOTICE:", n.strip())

    assert any("Monitor" in n for n in notices)
    assert any("Impresora" in n for n in notices)
    assert not any("Laptop" in n for n in notices)

  def test_actualizar_precio(db_connection):
    cur = db_connection.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio NUMERIC NOT NULL
    );
    CREATE TABLE IF NOT EXISTS auditoria_productos (
        id SERIAL PRIMARY KEY,
        producto_id INT NOT NULL,
        precio_anterior NUMERIC,
        precio_nuevo NUMERIC
    );
    """)

    cur.execute("DELETE FROM productos;")
    cur.execute("DELETE FROM auditoria_productos;")

    cur.execute("INSERT INTO productos (nombre, precio) VALUES ('Laptop', 1000) RETURNING id;")
    pid = cur.fetchone()[0]

    run_script(db_connection, "PROCEDURE_4.sql") 

    cur.execute("CALL actualizar_precio(%s, %s);", (pid, 1200))
    db_connection.commit()

    cur.execute("SELECT precio FROM productos WHERE id = %s;", (pid,))
    nuevo_precio = cur.fetchone()[0]
    assert nuevo_precio == 1200, "El precio no fue actualizado correctamente."

    cur.execute("""
        SELECT precio_anterior, precio_nuevo
        FROM auditoria_productos
        WHERE producto_id = %s;
    """, (pid,))
    auditoria = cur.fetchone()
    assert auditoria == (1000, 1200), f"Auditoría incorrecta: {auditoria}"

    cur.close()
