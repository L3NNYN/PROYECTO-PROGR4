from flask import jsonify, request, render_template, redirect, session, flash
from init import app
from init import mysql

@app.route('/tienda')
@app.route('/tienda/<int:id>', methods=['GET'])
def tienda(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if 'usuario' in session:
            cur.execute("SELECT t.nombre, t.direccion, t.foto, t.email FROM tbl_usuarios t WHERE t.estado = 'A' AND t.id_usr = %s", (session['id'],))
            row = cur.fetchone()
            data = []
            data.append({'nombre': row[0], 'direccion': row[1], 'foto': row[2], 'email': row[3], 'id': session['id']})
        return render_template("views/tienda.html", item=data)
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

#Productos mas vendidos y todos los productos de una tienda
@app.route('/tienda_api', methods=['GET'])
def getProductos():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        productos = []
        if 'usuario' in session:
            cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, %s), t.precio, t.tiempoEnvio, t.costoEnvio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.usr_id = %s", ("%d %M %Y",session['id'],))
            rows = cur.fetchall()
            for item in rows:
                productos.append({'id': item[0], 'descripcion': item[1], 'stock': item[2], 'publicacion': item[3], 'precio': item[4], 'tiempoEnvio': item[5], 'costoEnvio': item[6], 'categoria': item[7], 'tienda_id': item[8]})
        data = []
        data.append(productos)
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()
