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

@app.route('/carrito_api', methods=['GET', 'POST'])
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
        elif request.method == 'POST':
            _json = request.get_json(force=True)
            _metodopago = _json['metodo_pago']
            _direccionenvio = _json['direccion_envio']
            _comprador = session['id']

            evaluados = []
            for p in session['carrito']:
                _tienda = p['tienda_id']

                if not _tienda in evaluados: #
                    evaluados.append(_tienda)
                    # cur.execute("INSERT INTO tbl_compras (fecha, id_pago, id_comprador, id_dire, id_tienda) VALUES (now(), %s, %s, %s, %s)", (_metodopago, _comprador, _direccionenvio,_tienda))
                else:
                    print('ya esta')
            # if len(session['carrito']) != '':
            #     cur.execute("SELECT ")
            # else:
            #     return jsonify('No hay productos en la canasta')
            session['carrito'] = []

            return jsonify('Pago completado exitosamente')
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
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
        res = jsonify('Producto removido.')
        
        res.status_code = 200
        return res 
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error.')

