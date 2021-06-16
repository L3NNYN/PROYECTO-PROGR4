from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app
import bcrypt

@app.route('/metodos_pago', methods=['GET'])
def metod():
    try:
        if request.method == 'GET':
            return render_template('views/metodos_pago.html')
            # return render_template('views/metodos_pago.html')
    except Exception as e:
        print(e)

#Se accede desde Axios
@app.route('/metodos_pago_api', methods=['GET', 'POST'])
def data():
    try:
        cur = mysql.connect().cursor()

        if request.method == 'GET':
            cur.execute("SELECT id_pago, nombrePropietario, numero, cvv, fechaVencimiento, saldo FROM tbl_metodosdepago WHERE usr_id=%s", (session['id'],))
            rows = cur.fetchall()
            json_items = []
            content = {}
            # json_items.append({'id':'eho', 'propietario': 'asd', 'numero': "result[2]",  'cvv': 'result[3]', 'fecha': 'result[4]', 'saldo': 'result[5]'})
            for result in rows:
                content = {'id': result[0], 'propietario': result[1], 'numero': result[2],  'cvv': result[3], 'fecha': result[4], 'saldo': result[5]}
                json_items.append(content)
                content = {}
            return jsonify(json_items)

        elif request.method == 'POST': #Se agregan con Axios
            query = ("INSERT INTO tbl_metodosDePago (nombrePropietario, numero, cvv, fechaVencimiento, saldo, usr_id) VALUES (%s, %s, %s, %s, %s, %s)")

            _json = request.get_json(force=True) 
            _nombre = _json['propietario']
            _numero = _json['numero']
            _cvv = bcrypt.hashpw(_json['cvv'].encode('utf8'), bcrypt.gensalt(10))
            _fecha = _json['fecha']
            _saldo = _json['saldo']
            data = (_nombre, _numero, _cvv, _fecha, _saldo, session['id'],)

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()

            res = jsonify('Metodo de pago ingresado correctamente')
            res.status_code = 200
            return res
    except Exception as e:
        print(e)
    finally:
        cur.close()