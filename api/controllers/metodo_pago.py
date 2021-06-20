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

@app.route('/validar_cvv_api', methods=['POST'])
def cvv():
    try:
        if 'usuario' in session: 
            conn = mysql.connect()
            cur = conn.cursor()
            _json = request.get_json(force=True) 

            _metodopago = _json['metodo_pago']
            _cvv = _json['cvv']

            cur.execute("SELECT t.cvv FROM tbl_metodosdepago t WHERE t.id_pago = %s AND t.usr_id = %s", (_metodopago, session['id'],))
            row = cur.fetchone()
            if row and bcrypt.checkpw(_cvv.encode('utf8'), row[0].encode('utf8')):
                return jsonify({'valido': 'T'})
            else:
                return jsonify({'valido': 'F'})

        else:
            return jsonify('Deberias ingresar como comprador')
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error')
    finally:
        cur.close()

#Verifica que el metodo de pago tenga el monto suficiente
@app.route('/validar_monto_api', methods=['POST'])
def validarPago():
    try:
        cur = mysql.connect().cursor()
        if 'usuario' in session and 'C' == session['tipo_usuario']:
            _json = request.get_json(force=True)
            _id = _json['metodo_pago']
            _monto = _json['monto']

            cur.execute("SELECT 'S' FROM tbl_metodosdepago WHERE id_pago = %s AND saldo >= %s", (_id, _monto,))
            if cur.fetchone() != None:
                return jsonify('T')
            else:
                return jsonify('F')
        else:
            return jsonify('Registrate como comprador')

    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error en validar')
    finally:
        cur.close()

@app.route('/update_monto_api', methods=['PUT'])
def updateMonto():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if 'usuario' in session and 'C' == session['tipo_usuario']:
            _json = request.get_json(force=True)
            _id = _json['metodo_pago']
            _monto= _json['monto']
            
            cur.execute("UPDATE tbl_metodosdepago SET saldo = (saldo - %s) WHERE id_pago = %s", (_monto,_id,))
            conn.commit()

            return jsonify('Saldo de tu metodo de pago actualizado correctamente')
        else:
            return jsonify('Registrate como comprador')
    except Exception as e:
        print(e)
        return jsonify('Ha ocurrido un error en actualizar')
    finally:
        cur.close()

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