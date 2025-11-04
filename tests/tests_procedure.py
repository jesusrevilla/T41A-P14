import psycopg2
import pytest
from pathlib import Path

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
    yield conn
    conn.close()

def run_query_from_file(conn, filename):
    sql_path = Path(filename)
    with open(sql_path, "r") as file:
        query = file.read()
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def test_inner_join(db_connection):
    result = run_query_from_file(db_connection, "03_inner_join.sql")
    names = [row[0] for row in result]
    assert "Ana" in names and "Luis" in names
    assert "Carlos" not in names

def test_left_join(db_connection):
    result = run_query_from_file(db_connection, "04_left_join.sql")
    names = [row[0] for row in result]
    assert set(names) == {"Ana", "Luis", "Carlos"}

def test_right_join(db_connection):
    result = run_query_from_file(db_connection, "05_right_join.sql")
    products = [row[1] for row in result]
    assert "Phone" in products

def test_full_outer_join(db_connection):
    result = run_query_from_file(db_connection, "06_full_outer_join.sql")
    names = [row[0] for row in result]
    products = [row[1] for row in result]
    assert "Carlos" in names
    assert "Phone" in products
