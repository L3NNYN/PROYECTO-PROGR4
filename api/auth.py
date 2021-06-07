from flask import jsonify, request
from init import app
from init import mysql
import bcrypt

@app.route('/login', methods=['POST']) #Sólo podrá ser accedida vía POST 
def login(): 
    try: 
        _json = request.get_json(force=True) #Obtiene en formato JSON los datos enviados desde el front-End
        _usuario = _json['usuario']
        _password = _json['password']
        cur = mysql.connect().cursor()
        cur.execute("SELECT t.usuario, t.password FROM tbl_usuarios t WHERE usuario = %s", ('asd'))
        rows = cur.fetchone()
        # for result in rows:
        if bcrypt.checkpw(_password.encode('utf8'), rows[1].encode('utf8')):
            res = jsonify('Autenticacion exitosa') #Se retorna un mensaje de éxito en formato JSON 
        else:
            res = jsonify('Autenticacion erronea')
        res.status_code = 200 
        return res 
    except Exception as e: 
        res = jsonify('Ha ocurrido un error')
        print(e)
        res.status_code = 200 
        return res 
    finally: 
        print('asd')
        cur.close()


@app.route('/signup', methods=['POST']) #Sólo podrá ser accedida vía PUT 
def singup(): 
    try: 
        _json = request.get_json(force=True)
        _usuario = _json['usuario']
        _password = bcrypt.hashpw(_json['password'].encode('utf8'), bcrypt.gensalt(10)) #se encripta la contraseña
        _tipo = _json['tipo']
        query = "INSERT INTO tbl_usuarios(usr_id,usuario, password, tipo_usuario) VALUES (%s,%s, %s, %s)"
        data = (1,_usuario, _password, _tipo,)
        conn = mysql.connect() 
        cur = conn.cursor() 
        cur.execute(query, data) 
        conn.commit() 
        res = jsonify('Registrado exitosamente')
        res.status_code = 200 
        return res 
    except Exception as e: 
        res = jsonify('Ha ocurrido un error')
        print(e.args[0])
        res.status_code = 200 
        return res 
    finally: cur.close()

@app.route('/delete_productos/<int:id>', methods=['DELETE']) #Sólo podrá ser accedida vía DELETE 
def delete_productos(id): 
    try:
        # conn = mysql.connect() 
        # cur = conn.cursor() 
        # cur.execute("DELETE FROM tbl_productos WHERE id=%s", (id,)) 
        # conn.commit() 
        res = jsonify('Producto eliminado exitosamente.') 
        res.status_code = 200 
        return res 
    except Exception as e: 
        print(e) 
    finally: 
        print('jeje')
        # cur.close()

