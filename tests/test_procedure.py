import psycopg2

def test_procedure_delete():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    conn.autocommit = False
    try: 
        cur = conn.cursor()
        #Llamada incorrecta ID no valido
        cur.execute("CALL eliminar_producto(100);")
        #Uso de select para tomar los notices
        cur.execute("SELECT 1;")
        #Llamada correcta
        cur.execute("CALL eliminar_producto(3);")
        cur.execute("SELECT 1;")
        conn.commit()
        mensajes=conn.notices
        assert 'id incorrecto' in mensajes[0]
        assert 'eliminado correctamente' in mensajes[1]
        cur.execute("SELECT COUNT(*) FROM productos WHERE id=3;")
        count = cur.fetchone()[0]
        assert count == 0
    except Exception as e:
        raise e
    finally:
        #En caso de cualquier fallo en el try, el finally hará la limpieza.
        cur.close()
        conn.rollback()
        conn.close()

def test_procedure_update():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    conn.autocommit = False
    try:
        cur = conn.cursor()
        #Se obtiene precio anterior
        cur.execute("select precio from productos where id=1");
        resultadoAnt=cur.fetchone()[0];
        #Llamada para actualizar
        cur.execute("CALL actualizar_precio(0.15)")
        conn.commit()
        #Se obtiene precio actual
        cur.execute("select precio from productos where id=1");
        resultadoAct=cur.fetchone()[0];
        #comparacion
        porcentaje_cambio = (resultadoAct - resultadoAnt) / resultadoAnt
        assert abs(float(porcentaje_cambio) - 0.15) < 0.0001
    except Exception as e:
        raise e
    finally:
        #En caso de cualquier fallo en el try, el finally hará la limpieza.
        cur.close()
        conn.rollback()
        conn.close()

"""
def test_procedure_rango():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    #Se obtienen los registros que devulve el procedure
    cur.execute("select id,nombre precio from rango_precios(100.00,200.00)");
    resultados=cur.fetchall();
    assert len(resultados)==2;
    cur.close()
    conn.close()

def test_procedure_auditoria():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()
    cur.execute("select count(*) as total from auditoria;");
    auditoriaAnt=cur.fetchone()[0];
    cur.execute("update productos set precio=15.0 where id=2;");
    cur.execute("select count(*) as total from auditoria;");
    auditoriaAct=cur.fetchone()[0];
    assert auditoriaAct-auditoriaAnt==1;
    cur.close()
    conn.close()
"""



