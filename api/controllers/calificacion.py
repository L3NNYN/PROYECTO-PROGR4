from flask import jsonify, request, render_template, redirect, session, flash
from init import app
from init import mysql

@app.route('/calificacion_tienda_api/<int:id>', methods=['GET', 'POST', 'PUT'])
def calificacionTienda(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if id == None and not 'usuario' in session:
            return jsonify('Loggueate')
        else:
            if request.method == 'GET':
                
                data = []
                cur.execute("SELECT t.calificacion FROM calificaciontienda t WHERE t.id_comprador = %s AND t.id_tienda = %s", (session['id'], id,))
                if cur.rowcount != 0:
                    row = cur.fetchone()
                    data.append({'dada':int(row[0])})
                else:
                    data.append({'dada':'0'})

                # cur.execute("SELECT SUM(c.calificacion) / COUNT(c.calificacion) FROM tbl_usuarios t LEFT JOIN calificaciontienda c ON c.id_tienda = t.id_usr WHERE t.estado = 'A' AND t.id_usr = %s", (id,))
                cur.execute("SELECT SUM(c.calificacion) / COUNT(c.calificacion) FROM calificaciontienda c WHERE c.id_tienda = %s", (id,))
                row = cur.fetchone()
                if row[0] != None:
                    data.append({'tienda':float(row[0])})
                else:
                    data.append({'tienda': '0'})

                return jsonify(data)

            elif request.method == 'POST':
                _json = request.get_json(force= True)
                _calificacion = _json['calificacion']
                _comprador = session['id']
                _tienda = id
                
                cur.execute("INSERT INTO calificaciontienda (id_comprador, id_tienda, calificacion) VALUES (%s, %s, %s)", (_comprador, _tienda, _calificacion,))
                conn.commit()
                
                return jsonify('Calificacion ingresada correctamente')

            elif request.method == 'PUT':
                _json = request.get_json(force= True)
                _calificacion = _json['calificacion']
                _comprador = session['id']
                _tienda = id
                
                cur.execute("UPDATE calificaciontienda SET calificacion = %s WHERE id_comprador = %s AND id_tienda = %s", (_calificacion, _comprador, _tienda, ))
                conn.commit()
                
                return jsonify('Calificacion actualizada correctamente')

    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/calificacion_producto_api/<int:id>', methods=['GET', 'POST', 'PUT'])
def calificacionProducto(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if id == None and not 'usuario' in session:
            return jsonify('Loggueate')
        else:
            if request.method == 'GET':
                
                data = []
                cur.execute("SELECT calificacion FROM calificacionproducto WHERE usr_id = %s AND id_producto = %s", (session['id'], id,))
                if cur.rowcount != 0:
                    row = cur.fetchone()
                    data.append({'dada':int(row[0])})
                else:
                    data.append({'dada':'0'})

                cur.execute("SELECT SUM(c.calificacion) / COUNT(c.calificacion) FROM calificacionproducto c WHERE c.id_producto = %s", (id,))
                row = cur.fetchone()
                if row[0] != None:
                    data.append({'producto':float(row[0])})
                else:
                    data.append({'producto': '0'})

                return jsonify(data)

            elif request.method == 'POST':
                _json = request.get_json(force= True)
                _calificacion = _json['calificacion']
                _comprador = session['id']
                _tienda = id
                
                cur.execute("INSERT INTO calificacionproducto (usr_id, id_producto, calificacion) VALUES (%s, %s, %s)", (_comprador, _tienda, _calificacion,))
                conn.commit()
                
                return jsonify('Calificacion ingresada correctamente')

            elif request.method == 'PUT':
                _json = request.get_json(force= True)
                _calificacion = _json['calificacion']
                _comprador = session['id']
                _tienda = id
                
                cur.execute("UPDATE calificacionproducto SET calificacion = %s WHERE usr_id = %s AND id_producto = %s", (_calificacion, _comprador, _tienda, ))
                conn.commit()
                
                return jsonify('Calificacion actualizada correctamente')
    except Exception as e:
        print(e)
    finally:
        cur.close()