from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

@app.route('/redes_sociales')
def redes():
    try: 
        return render_template('views/redes_sociales.html')
    except Exception as e:
        print(e)
        return redirect('/inicio')

#Mantenimiento de redes sociales 
@app.route('/redes_sociales_api', methods=['GET', 'POST', 'PUT'])
@app.route('/redes_sociales_api/<int:id>', methods=['DELETE'])
def redes_api(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if not 'usuario' in session:
            return jsonify('Deberias loguearte')
        elif session['tipo_usuario'] == 'T':

            if request.method == 'GET':
                cur.execute("SELECT t.id_reds, t.descripcion FROM tbl_redessociales t WHERE t.usr_id = %s", (session['id'], ))
                rows = cur.fetchall()
                json_items = []
                content = {}
                for result in rows:
                    content = {'id': result[0], 'descripcion': result[1]}
                    json_items.append(content)
                    content = {}
                return jsonify(json_items)

            elif request.method == 'POST':

                _json = request.get_json(force=True)
                _descripcion = _json['descripcion']
                cur.execute("INSERT INTO tbl_redessociales (descripcion, usr_id) VALUES (%s, %s)", (_descripcion,session['id'],))
                conn.commit()

                return jsonify('Red social agregada correctamente.')

            elif request.method == 'PUT':

                _json = request.get_json(force=True)
                _descripcion = _json['descripcion']
                _id = _json['id']
                cur.execute("UPDATE tbl_redessociales SET descripcion=%s WHERE id_reds = %s", (_descripcion,_id,))
                conn.commit()

                return jsonify('Red social actualizada correctamente correctamente.')

            elif request.method == 'DELETE':
                cur.execute("DELETE FROM tbl_redessociales WHERE id_reds = %s", (id,))
                conn.commit()
                return jsonify('Red social borrada correctamente correctamente.')
        else:
            return jsonify('No eres una tienda')

    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()