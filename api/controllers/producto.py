import os
from flask import jsonify, request, render_template, redirect, session
from werkzeug.utils import secure_filename
from init import mysql
from init import app

pathFotos = './static/img_productos'

@app.route('/productos', methods=['GET'])
def productos():
    try:
        cur = mysql.connect().cursor()
        if 'usuario' in session:
            print(session['usuario'])
            cur.execute("SELECT p.id_prod, p.descripcion, p.stock, DATE_FORMAT(p.publicacion, %s), p.precio, p.tiempoenvio, p.costoenvio, c.descripcion FROM tbl_productos p RIGHT JOIN tbl_categoriasproductos c ON c.id_catp = p.id_categoria WHERE p.usr_id = %s", (("%d %M %Y"),session['id'],))

            rows = cur.fetchall()
            items = []
            content = {}
            for result in rows:
                content = {'id': result[0], 'descripcion': result[1], 'stock': result[2], 'publicacion': result[3], 'precio':result[4], 'tiempoEnvio': result[5], 'costoEnvio': result[6], 'categoria': result[7]} #value = id, text = nombre del pais
                items.append(content)
            content ={}
            return render_template('views/productos.html', items=items)
        else:
            return redirect('/login')
    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/producto/<int:id>')
def producto(id=None):
    try:
        cur = mysql.connect().cursor()

        if not 'usuario' in session:
            return redirect('/login')

        if id == None:
            return redirect('/inicio')
        else:
            cur.execute("SELECT p.id_prod, p.usr_id, p.descripcion, p.stock, p.publicacion, p.precio, p.tiempoenvio, p.costoenvio, c.descripcion FROM tbl_productos p RIGHT JOIN tbl_categoriasproductos c ON c.id_catp = p.id_categoria WHERE p.id_prod =%s", (id,))
            result = cur.fetchone()
            items = []

            # Informacion del producto y sus fotos
            items.append({'id': result[0], 'tienda': result[1],'descripcion': result[2], 'stock': result[3], 'publicacion': result[4], 'precio':result[5], 'tiempoEnvio': result[6], 'costoEnvio': result[7], 'categoria': result[8]})
            cur.execute("SELECT path FROM tbl_fotos WHERE id_producto = %s", (id,))
            rows = cur.fetchall()
            fotos = []
            for data in rows:
                fotos.append({'path': data[0]})

            cur.execute("SELECT path FROM tbl_fotos WHERE id_producto = %s", (id,))
            rows = cur.fetchall()
            fotos = []
            for data in rows:
                fotos.append({'path': data[0]})
           

            return render_template('views/producto.html', items=items, fotos= fotos, len_f = len(fotos))
            # if session['tipo_usuario'] == 'C':
            # else:
            #     return render_template('views/producto.html', items=items, fotos= fotos, len_f = len(fotos))

    except Exception as e:
        print(e)
    finally:
       cur.close()

#recibe el id del producto y agrega un comentario via AXIOS
@app.route('/comentarios_api/<int:id>', methods=['POST', 'GET'])
def comentarios(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if request.method == 'GET':
            cur.execute("SELECT t.id_come, t.descripcion, u.nombre, u.foto FROM tbl_comentarios t LEFT JOIN tbl_usuarios u ON t.id_usr = u.id_usr WHERE t.id_producto = %s", (id,))
            rows = cur.fetchall()
            comentarios = []
            for data in rows:
                comentarios.append({'id': data[0], 'descripcion': data[1], 'usuario': data[2], 'foto': data[3]})
            return jsonify(comentarios)
        elif request.method == 'POST':
            _json = request.get_json(force=True)
            _descripcion = _json['descripcion']
            _producto = id
            _usuario = session['id']
             
            cur.execute("INSERT INTO tbl_comentarios (descripcion, id_producto, id_usr) VALUES (%s, %s, %s)", (_descripcion, _producto, _usuario,))
            conn.commit()

            return jsonify("Comentario agregado correctamente.")
    except Exception as e:
        print(e)
        return jsonify("Ha ocurrido un error.")
    finally:
        cur.close()

#Se ingresa el producto, con sus respectivas imagenes
@app.route('/nuevo_producto', methods=['GET','POST'])
def new_prod():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if 'usuario' in session:

            if request.method == 'GET':
                return render_template('views/nuevo_producto.html')

            elif request.method == 'POST':

                data = request.form
                _descripcion = data['descripcion']
                _stock = data['stock']
                _precio = data['precio']
                _tiempoEnvio = data['tiempoEnvio']
                _costoEnvio = data['costoEnvio']
                _categoria = data['categoria']

                query = ("INSERT INTO tbl_productos (descripcion, stock, publicacion, precio, tiempoEnvio, costoEnvio, id_categoria, usr_id) VALUES ( %s,%s,now(),%s,%s,%s,%s,%s)")
                values = (_descripcion, _stock, _precio, _tiempoEnvio, _costoEnvio, _categoria, session['id'])

                cur.execute(query, values)
                conn.commit()

                _idProducto = cur.lastrowid
                fotos = []
                files = request.files.getlist('foto')
                
                for f in files:
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(pathFotos, filename))
                    _foto = f.filename
                    fotos.append((_foto, _idProducto))

                if fotos:
                    query = ("INSERT INTO tbl_fotos (path, id_producto) VALUES (%s, %s)")
                    cur.executemany(query, fotos)
                    conn.commit()
                
                return redirect('/productos')
        else:
            msg = 'Debes iniciar sesion'
            return redirect('/login', info=msg)
    except Exception as e:
        print(e)
        return redirect('/nuevo_producto')
    finally:
        cur.close()


@app.route('/categorias_productos_api', methods=['GET','POST'])
def categorias():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if request.method == 'GET':
            cur.execute("SELECT * FROM tbl_categoriasproductos")
            rows = cur.fetchall()
            json_items = []
            content = {}
            for result in rows:
                content = {'value': result[0], 'text': result[1]} #value = id, text = nombre del pais
                json_items.append(content)
            content ={}
            return jsonify(json_items) #se retorna el formato JSON
        elif request.method == 'POST':
            _json = request.get_json(force=True)
            _descripcion = _json['descripcion']

            cur.execute("INSERT INTO tbl_categoriasproductos (descripcion) VALUES (%s)", (_descripcion,))
            conn.commit()

            res = jsonify('Categoria agregada correctamente')
            res.status_code = 200
            return res
    except Exception as e:
        print(e)
    finally:
        cur.close()



