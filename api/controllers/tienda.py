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
            if id == None:
                cur.execute("SELECT t.nombre, t.direccion, t.foto, t.email FROM tbl_usuarios t WHERE t.estado = 'A' AND t.id_usr = %s", (session['id'],))
                # cur.execute("SELECT t.nombre, t.direccion, t.foto, t.email, (SUM(c.calificacion) / COUNT(c.calificacion)) FROM tbl_usuarios t LEFT JOIN calificaciontienda c ON c.id_tienda = t.id_usr WHERE t.estado = 'A' AND t.id_usr = %s", (session['id'],))
            else:
                # cur.execute("SELECT t.nombre, t.direccion, t.foto, t.email, (SUM(c.calificacion) / COUNT(c.calificacion)) FROM tbl_usuarios t LEFT JOIN calificaciontienda c ON c.id_tienda = t.id_usr WHERE t.estado = 'A' AND t.id_usr = %s", (id,))
                cur.execute("SELECT t.nombre, t.direccion, t.foto, t.email FROM tbl_usuarios t WHERE t.estado = 'A' AND t.id_usr = %s", (id,))

            row = cur.fetchone()
            data = []
            profile = 'F'
            if session['id'] == id or id == None: profile = 'T' #si esta accediendo desde la navbar o desde el inicio
            
            if profile is 'T':
                data.append({'nombre': row[0], 'direccion': row[1], 'foto': row[2], 'email': row[3], 'id': session['id'], 'calificacion': float(row[4])})
            else:
                data.append({'nombre': row[0], 'direccion': row[1], 'foto': row[2], 'email': row[3], 'id': id})


        return render_template("views/tienda.html", item=data, profile=profile)
    except Exception as e:
        print(e)
        return redirect('/login')
    finally:
        cur.close()

#Productos mas vendidos y todos los productos de una tienda
@app.route('/tienda_api')
@app.route('/tienda_api/<int:id>')
def getProductos(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        productos = []
        if 'usuario' in session:
            if id == None:
                cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, %s), t.precio, t.tiempoEnvio, t.costoEnvio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.usr_id = %s", ("%d %M %Y",session['id'],))
            else:
                # if request.get_json is not None:
                cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, %s), t.precio, t.tiempoEnvio, t.costoEnvio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.usr_id = %s", ("%d %M %Y",id,))
                # else:
                    # cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, %s), t.precio, t.tiempoEnvio, t.costoEnvio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.usr_id = %s", ("%d %M %Y",id,))
            
            rows = cur.fetchall()
            for item in rows:
                productos.append({'id': item[0], 'descripcion': item[1], 'stock': item[2], 'publicacion': item[3], 'precio': item[4], 'tiempoEnvio': item[5], 'costoEnvio': item[6], 'categoria': item[7], 'tienda_id': item[8]})
        # data = []
        # data.append(productos)
        return jsonify(productos)
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

@app.route('/seguimiento_api/<int:id>', methods=['POST', 'GET'])
def seguimiento(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if not 'usuario' in session:
            return jsonify('Es necesario loguearse')
        else:
            res = ''
            if request.method == 'POST':
                _json = request.get_json(force=True)
                if _json['seguir'] == 'T':
                    cur.execute("INSERT INTO seguir (id_comprador, id_tienda) VALUES (%s, %s)", (session['id'], id))
                    conn.commit()
                    res = "Ahora sigues a esta tienda."
                elif _json['seguir'] == 'F':
                    cur.execute("DELETE FROM seguir WHERE id_comprador = %s AND id_tienda = %s", (session['id'], id))
                    conn.commit()
                    res = "Has dejado de seguir esta tienda."

            elif request.method == 'GET':
                cur.execute("SELECT * FROM seguir WHERE id_comprador = %s AND id_tienda = %s", (session['id'], id))
                row = cur.fetchone()
                if row:
                    res = 'T'
                else:
                    res = 'F'

        return jsonify(res)
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()
