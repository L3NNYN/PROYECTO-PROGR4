from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

#Se carga la vista de las direcciones de envio
@app.route('/direcciones_envio')
def direcciones():
    try:
        if 'usuario' in session and session['tipo_usuario'] == 'C':
            return render_template('views/direcciones_envio.html')
        else:
            return redirect('/login')
    except Exception as e:
        print(e)

#Mantenimiento de las direcciones de envio AXIOS
@app.route('/direcciones_envio_api', methods=['GET', 'POST', 'PUT'])
@app.route('/direcciones_envio_api/<int:id>', methods=['DELETE'])
def dir_data(id=None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if request.method == 'GET': #GET AXIOS
            cur.execute("SELECT t.id_dire, t.numCasillero, t.codPostal, t.provincia, p.descripcion, t.id_pais FROM tbl_direccionesdeenvio t JOIN tbl_Paises p ON t.id_pais = p.id_pais WHERE usr_id=%s", (session['id'],))
            rows = cur.fetchall()
            json_items = []
            content = {}

            for result in rows:
                content = {'id': result[0], 'casillero': result[1], 'codPostal': result[2],  'provincia': result[3], 'pais': result[4], 'id_pais': result[5]}
                json_items.append(content)
                content = {}
            return jsonify(json_items)

        elif request.method == 'POST': #Se agregan con Axios
            query = ("INSERT INTO tbl_direccionesdeenvio (numCasillero, codPostal, provincia, id_pais, usr_id) VALUES (%s, %s, %s, %s, %s)")

            _json = request.get_json(force=True) 
            _numCasillero = _json['numCasillero']
            _codPostal = _json['codPostal']
            _provincia = _json['provincia']
            _pais = _json['id_pais']
            data = (_numCasillero, _codPostal, _provincia, _pais, session['id'],)

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()

            res = jsonify('Direccion de envio ingresada correctamente')
            res.status_code = 200
            return res
        elif request.method == 'PUT': #UPDATE AXIOS
            query = ("UPDATE tbl_direccionesdeenvio SET numCasillero = %s, codPostal = %s, provincia = %s, id_pais = %s WHERE id_dire = %s")

            _json = request.get_json(force=True) 
            _numCasillero = _json['numCasillero']
            _codPostal = _json['codPostal']
            _provincia = _json['provincia']
            _pais = _json['id_pais']
            _id = _json['id']
            data = (_numCasillero, _codPostal, _provincia, _pais, _id,)

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()

            res = jsonify('Direccion actualizada')
            res.status_code = 200
            return res

        elif request.method == 'DELETE': #DELETE AXIOS

            cur.execute("DELETE FROM tbl_direccionesdeenvio WHERE id_dire = %s", (id,))
            conn.commit()
        
            return jsonify('Direccion borrada')
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()