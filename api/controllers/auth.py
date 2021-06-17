import os
from flask import jsonify, request, render_template, redirect, session
from werkzeug.utils import secure_filename
from init import mysql
from init import app

import bcrypt

@app.route('/login', methods=['POST', 'GET']) #Sólo podrá ser accedida vía POST 
@app.route('/login/<msg>')
def login():
    try: 
        cur = mysql.connect().cursor()

        if request.method == 'GET':
            return render_template('views/login.html')
        else:
            data = request.form
            # _json = request.get_json(force=True) #Obtiene en formato JSON los datos enviados desde el front-End
            _usuario = data['usuario']
            _password = data['password']
            cur.execute("SELECT t.usuario, t.password, t.nombre, t.tipo_usuario, t.id_usr FROM tbl_usuarios t WHERE usuario = %s", (_usuario))
            rows = cur.fetchone()
            if rows and bcrypt.checkpw(_password.encode('utf8'), rows[1].encode('utf8')):
                session.permanent = False
                session['carrito'] = []
                session['usuario'] = rows[0]
                session['nombre'] = rows[2]
                session['tipo_usuario'] = rows[3]
                session['id'] = rows[4]
                return redirect('/inicio')
            else:
                m = "Credenciales incorrectas"
                return redirect('/login')
            # return redirect('/login', msg='wenas')
    except Exception as e: 
        res = jsonify('Ha ocurrido un error: ')
        print(e)
        res.status_code = 200 
        return res 
    finally: 
        print('/login')
        cur.close()

@app.route('/signup', methods=['POST']) #Sólo podrá ser accedida vía POST
def singup(): 
    try: 
        data = request.form
        _nombre = data['nombre']
        _cedula = data['cedula']
        # _telefono = data['telefono'] #FALTA DE AGREGAR 
        _email = data['email']
        _direccion = data['direccion']
        _pais = data['pais']
        _tipo = data['tipo']
        _usuario = data['usuario']
        _password = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt(10)) #se encripta la contraseña

        f = request.files['foto']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        _foto = f.filename

        query = "INSERT INTO tbl_usuarios(nombre, cedula, email, direccion, id_pais, foto, tipo_usuario, usuario, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (_nombre, _cedula,_email, _direccion, _pais, _foto, _tipo, _usuario, _password,)
        conn = mysql.connect() 
        cur = conn.cursor() 
        cur.execute(query, values) 
        conn.commit() 
        
        return redirect('/inicio')
    except Exception as e: 
        res = jsonify('Ha ocurrido un error')
        print(e)
        res.status_code = 200 
        return res 
    finally: 
        cur.close()

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('views/signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    session.pop('id', None)
    session.pop('tipo_usuario', None)
    session.pop('nombre', None)
    session.pop('canasta', None)

    return redirect('/login')