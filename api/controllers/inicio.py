from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

@app.route('/todo_productos_api')
@app.route('/todo_productos_api/<string:filter>')
def todoProductos(filter=None):
    try:
        cur = mysql.connect().cursor()
        if filter == None:
            cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, '%d %M %Y'), t.precio, c.descripcion FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria")
        else:
            cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, %s), t.precio, c.descripcion FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.descripcion LIKE  %s OR c.descripcion = %s", ("%d %M %Y","%" + filter +"%", filter,))

        rows = cur.fetchall()
        json_items = []
        content = {}
        for result in rows:
            content = {'id': result[0], 'descripcion': result[1], 'stock': result[2], 'fechapublicacion': result[3], 'precio': result[4], 'categoria': result[5]} #value = id, text = nombre del pais
            json_items.append(content)
        
        return jsonify(json_items)
    except Exception as e:
        print(e)
    finally:
        cur.close()


@app.route('/todo_tiendas_api')
@app.route('/todo_tiendas_api/<string:filter>')
def todoTiendas(filter = None):
    try:
        cur = mysql.connect().cursor()
        if filter == None:
            cur.execute("SELECT t.id_usr, t.nombre, t.foto  FROM tbl_usuarios t WHERE t.tipo_usuario = 'T'")
        else:
            cur.execute("SELECT t.id_usr, t.nombre, t.foto  FROM tbl_usuarios t WHERE t.tipo_usuario = 'T' AND t.nombre LIKE %s", ("%"+ filter +"%",))
        rows = cur.fetchall()
        json_items = []
        content = {}
        for result in rows:
            content = {'id': result[0], 'nombre': result[1], 'foto': result[2]} #value = id, text = nombre del pais
            json_items.append(content)
        
        return jsonify(json_items)
    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/mas_vendidos_api')
def mas_vendidos():
    try:
        cur = mysql.connect().cursor()
        cur.execute("SELECT t.id_usr, t.nombre, t.foto  FROM tbl_usuarios t WHERE t.tipo_usuario = 'T'")
        rows = cur.fetchall()
        json_items = []
        content = {}
        for result in rows:
            content = {'id': result[0], 'nombre': result[1], 'foto': result[2]} #value = id, text = nombre del pais
            json_items.append(content)
        
        return jsonify(json_items)
    except Exception as e:
        print(e)
    finally:
        cur.close()