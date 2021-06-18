from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

@app.route('/carrito')
def carrito():
    try:
        if 'usuario' in session:
            return render_template('views/carrito.html')
        else:
            return redirect('/login')
    except Exception as e:
        print(e)


@app.route('/carrito_api', methods=['GET', 'PUT'])
def carrito_api():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if not 'usuario' in session:
            return jsonify('Deberias loggearte')
        
        productos = []
        if request.method == 'GET':
            if len(session['carrito']) != '':
                for p in session['carrito']:
                    cur.execute("SELECT t.descripcion, t.precio, c.descripcion, t.tiempoenvio, t.costoenvio, u.nombre, t.id_prod, u.id_usr FROM tbl_productos t LEFT JOIN tbl_categoriasproductos c ON c.id_catp = t.id_categoria LEFT JOIN tbl_usuarios u ON u.id_usr = t.usr_id WHERE t.id_prod = %s ", (p['id'],))
                    item = cur.fetchone()
                    if item:
                        productos.append({'descripcion': item[0], 'precio': item[1], 'categoria': item[2], 'tiempo envio': item[3], 'costo envio': item[4], 'tienda': item[5], 'id': item[6], 'tienda_id': item[7]})
            return jsonify(productos)
    except Exception as e:
        print(e)
    finally:
        cur.close()

#Agrega items al carrito via AXIOS
@app.route('/add_carrito_api', methods=['POST'])
def canasta():
    try:
        _json = request.get_json(force=True)
        _id = _json['id']
        _tienda = _json['tienda_id']
        session['carrito'].append({'id':_id, 'tienda_id': _tienda})

        res = jsonify('Producto agregado al carrito correctamente.')
        res.status_code = 200
        return res 
    except Exception as e:
        print(e)
        res = jsonify('Ha ocurrido un error.')
        return res 

#Remueve items del carrito via AXIOS
@app.route('/remover_carrito_api', methods=['POST'])
def canasta2():
    try:
        _json = request.get_json(force=True)
        _id = _json['id']
        _tiendaid = _json['tienda_id']

        session['carrito'].remove({'id':_id, 'tienda_id': _tiendaid})
        res = jsonify('Producto eliminado del carrito correctamente.')
        
        res.status_code = 200
        return res 
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error.')

