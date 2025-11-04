import psycopg2

def test_procedure_delete():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("CALL eliminar_producto(100)")
    cur.execute("CALL eliminar_producto(2)")
    mensajes=conn.notices
    assert 'id incorrecto' in mensajes[0]
    assert 'eliminado correctamente' in mensajes[1]
    cur.close()
    conn.close()

def test_procedure_delete():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("CALL actualizar_precio(0.15)")
    cur.execute("select precio from productos where id=1");
    
    assert 'id incorrecto' in mensajes[0]
    assert 'eliminado correctamente' in mensajes[1]
    cur.close()
    conn.close()
