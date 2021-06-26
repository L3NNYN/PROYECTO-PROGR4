from flask import jsonify, request, render_template, redirect, session, flash
from init import app
from init import mysql

#Metodo para obtener la tienda, por id o si la el usuario es tipo tienda
@app.route('/tienda')
@app.route('/tienda/<int:id>', methods=['GET'])
def tienda(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        
        if 'usuario' in session:
            if id == None:
                cur.execute("SELECT t.nombre, t.direccion, t.foto, t.email, p.descripcion FROM tbl_usuarios t LEFT JOIN tbl_paises p ON p.id_pais = t.id_pais WHERE t.estado = 'A' AND t.id_usr = %s", (session['id'],))
            else:
                cur.execute("SELECT t.nombre, t.direccion, t.foto, t.email, p.descripcion FROM tbl_usuarios t LEFT JOIN tbl_paises p ON p.id_pais = t.id_pais WHERE t.estado = 'A' AND t.id_usr = %s", (id,))

            row = cur.fetchone()
            data = []
            profile = 'F'
            if session['id'] == id or id == None: profile = 'T' #si esta accediendo desde la navbar o desde el inicio
            
            if profile is 'T':
                data.append({'nombre': row[0], 'direccion': row[1], 'foto': row[2], 'email': row[3], 'pais':row[4],'id': session['id']})
            else:
                data.append({'nombre': row[0], 'direccion': row[1], 'foto': row[2], 'email': row[3], 'pais':row[4], 'id': id})


        return render_template("views/tienda.html", item=data, profile=profile)
    except Exception as e:
        print(e)
        return redirect('/login')
    finally:
        cur.close()

#Todos los productos de una tienda
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
        return jsonify(productos)
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

@app.route('/search_tienda_api/<string:filter>/<int:id>')
def searchTienda(filter=None, id =None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if filter == None:
            cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, '%d %M %Y'), t.precio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria")
        else:
            cur.execute("SELECT t.id_prod, t.descripcion, t.stock, DATE_FORMAT(t.publicacion, %s), t.precio, t.tiempoenvio, t.costoenvio, c.descripcion, t.usr_id FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria WHERE t.usr_id = %s AND t.descripcion LIKE  %s OR c.descripcion = %s", ("%d %M %Y",id,"%" + filter +"%", filter,))
        
        rows = cur.fetchall()
        print(rows)
        json_items = []
        content = {}
        for result in rows:
            content = {'id': result[0], 'descripcion': result[1], 'stock': result[2], 'publicacion': result[3], 'precio': result[4], 'tiempoEnvio': result[5], 'costoEnvio': result[6], 'categoria': result[7], 'tienda_id': result[8]} #value = id, text = nombre del pais
            json_items.append(content)
        
        return jsonify(json_items)
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

#Funcion API para seguir o dejar de seguir a una tienda
@app.route('/seguimiento_api/<int:id>', methods=['POST', 'GET'])
def seguimiento(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if not 'usuario' in session:
            return jsonify('Es necesario loguearse')
        else:
            res = ''
            if request.method == 'POST': #POST AXIOS
                _json = request.get_json(force=True)
                if _json['seguir'] == 'T':
                    cur.execute("INSERT INTO seguir (id_comprador, id_tienda) VALUES (%s, %s)", (session['id'], id))
                    conn.commit()
                    res = "Ahora sigues a esta tienda."
                elif _json['seguir'] == 'F':
                    cur.execute("DELETE FROM seguir WHERE id_comprador = %s AND id_tienda = %s", (session['id'], id))
                    conn.commit()
                    res = "Has dejado de seguir esta tienda."

            elif request.method == 'GET': #AXIOS GET
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

#Retornar los seguidores de la tienda
@app.route('/get_seguidores_api/<int:id>')
def getSeguidores(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if not 'usuario' in session:
            return jsonify('Debes iniciar sesion')

        data=[]
        cur.execute("SELECT s.id_comprador, u.nombre FROM seguir s LEFT JOIN tbl_usuarios u ON s.id_comprador = u.id_usr WHERE s.id_tienda = %s", (id,))
        rows = cur.fetchall()
        for row in rows:
            data.append({'id': row[0], 'nombre': row[1]})

        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify('ocurrio un error')
    finally:
        cur.close()

#REtorna los productos en lista de desesos
@app.route('/productos_listadeseos_api/<int:id>')
def getListasDeseos(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if not 'usuario' in session:
            return jsonify('Debes iniciar sesion')

        data=[]
        cur.execute("SELECT s.usr_id, u.nombre, p.descripcion FROM listadeseos s LEFT JOIN tbl_usuarios u ON s.usr_id = u.id_usr LEFT JOIN tbl_productos p ON p.id_prod = s.id_producto WHERE p.usr_id  = %s", (id))
        rows = cur.fetchall()
        print(rows)
        for row in rows:
            data.append({'id': row[0], 'nombre': row[1], 'producto': row[2]})

        return jsonify(data)

    except Exception as e:
        print(e)
        return jsonify('ocurrio un error')
    finally:
        cur.close()
