from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

@app.route('/direcciones_envio')
def direcciones():
    try:
        return render_template('views/direcciones_envio.html')
    except Exception as e:
        print(e)

@app.route('/direcciones_envio_api', methods=['GET', 'POST', 'PUT'])
def dir_data():
    try:
        cur = mysql.connect().cursor()

        if request.method == 'GET':
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
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()