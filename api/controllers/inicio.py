from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

@app.route('/todo_productos_api')
@app.route('/todo_productos_api/<string:filter>')
def todoProductos(filter=None):
    try:
        cur = mysql.connect().cursor()
        if filter == None:
            cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, '%d %M %Y'), t.precio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria")
        else:
            cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, %s), t.precio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.descripcion LIKE  %s OR c.descripcion = %s", ("%d %M %Y","%" + filter +"%", filter,))

        rows = cur.fetchall()
        json_items = []
        content = {}
        for result in rows:
            content = {'id': result[0], 'descripcion': result[1], 'stock': result[2], 'fechapublicacion': result[3], 'precio': result[4], 'categoria': result[5], 'tienda_id': result[6]} #value = id, text = nombre del pais
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
            cur.execute("SELECT t.id_usr, t.nombre, t.foto  FROM tbl_usuarios t WHERE t.tipo_usuario = 'T' ORDER BY t.nombre DESC")
        else:
            cur.execute("SELECT t.id_usr, t.nombre, t.foto  FROM tbl_usuarios t WHERE t.tipo_usuario = 'T' AND t.nombre LIKE %s ORDER BY t.nombre DESC", ("%"+ filter +"%",))
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
@app.route('/mas_vendidos_api/<string:filter>')
def masVendidos(filter = None):
    try:
        cur = mysql.connect().cursor()
        if filter == None:
            cur.execute("SELECT t.id_prod,t.descripcion, t.precio, c.descripcion, DATE_FORMAT(t.publicacion,'%d %M %Y'), SUM(p.cantidad), t.usr_id FROM productos p LEFT JOIN tbl_productos t ON t.id_prod = p.id_prod LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria GROUP BY p.id_prod ORDER BY SUM(p.cantidad) DESC LIMIT 5")
        else:
            query = "SELECT t.id_prod,t.descripcion, t.precio, c.descripcion, DATE_FORMAT(t.publicacion, %s), SUM(p.cantidad), t.usr_id FROM productos p LEFT JOIN tbl_productos t ON t.id_prod = p.id_prod LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.descripcion LIKE  %s OR c.descripcion = %s GROUP BY p.id_prod ORDER BY SUM(p.cantidad) DESC LIMIT 5"
            values = ("%d %M %Y", "%"+filter +"%", filter)
            cur.execute(query, values)
        rows = cur.fetchall()
        data = []
        for row in rows:
            data.append({'id':row[0], 'descripcion':row[1], 'precio':row[2], 'categoria':row[3], 'fechapublicacion':row[4],'vendido':float(row[5]), 'tienda_id':row[6]})
        
        return jsonify(data)
    except Exception as e:
        print(e)
    finally:
        cur.close()