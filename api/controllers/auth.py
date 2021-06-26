import os
from flask import jsonify, request, render_template, redirect, session
from werkzeug.utils import secure_filename
from init import mysql
from init import app

import bcrypt

#Metodo para login
@app.route('/login', methods=['POST', 'GET']) 
def login():
    try: 
        cur = mysql.connect().cursor()

        if request.method == 'GET':
            return render_template('views/login.html')
        elif request.method == 'POST':
            data = request.form
            _usuario = data['usuario']
            _password = data['password']
            cur.execute("SELECT t.usuario, t.password, t.nombre, t.tipo_usuario, t.id_usr FROM tbl_usuarios t WHERE usuario = %s", (_usuario))
            rows = cur.fetchone()
            if rows and bcrypt.checkpw(_password.encode('utf8'), rows[1].encode('utf8')): #se encripta el password
                #Se guardan variables globales
                session.permanent = False
                session['carrito'] = []
                session['usuario'] = rows[0]
                session['nombre'] = rows[2]
                session['tipo_usuario'] = rows[3]
                session['id'] = rows[4]

                return redirect('/inicio')
            else:
                return redirect('/login')
    except Exception as e: 
        res = jsonify('Ha ocurrido un error: ')
        print(e)
        res.status_code = 200 
        return res 
    finally: 
        print('/login')
        cur.close()

#Metodo para signup
@app.route('/signup', methods=['POST']) 
def singup(): 
    try:
        conn = mysql.connect() 
        cur = conn.cursor() 
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

        #se crean las fotos
        f = request.files['foto']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        _foto = f.filename

        query = "INSERT INTO tbl_usuarios(nombre, cedula, email, direccion, id_pais, foto, tipo_usuario, usuario, password, estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"
        values = (_nombre, _cedula,_email, _direccion, _pais, _foto, _tipo, _usuario, _password,'A',)
        cur.execute(query, values) 
        conn.commit() 
        
        return redirect('/login')
    except Exception as e: 
        res = jsonify('Ha ocurrido un error')
        print(e)
        res.status_code = 200 
        return redirect('/signup') 
    finally: 
        cur.close()

#se envia la vista de signup
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('views/signup.html')

#Se borran las variables globales
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    session.pop('id', None)
    session.pop('tipo_usuario', None)
    session.pop('nombre', None)
    session.pop('canasta', None)

    return redirect('/login')