import os
from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app
from werkzeug.utils import secure_filename

#Obtiene el perfil del usuario comprador
@app.route('/perfil')
@app.route('/perfil/<int:id>')
def pefil(id=None):
    try:
        cur = mysql.connect().cursor()
        
        if id != None:
            cur.execute("SELECT t.nombre, t.usuario, t.cedula, t.email, t.direccion, p.descripcion, t.foto, t.tipo_usuario, t.id_usr FROM tbl_usuarios t LEFT JOIN tbl_paises p ON p.id_pais = t.id_pais WHERE t.id_usr=%s", (id,))
        else:
            cur.execute("SELECT t.nombre, t.usuario, t.cedula, t.email, t.direccion, p.descripcion, t.foto, t.tipo_usuario, t.id_usr FROM tbl_usuarios t LEFT JOIN tbl_paises p ON p.id_pais = t.id_pais WHERE t.id_usr=%s", (session['id'],))

        usr = cur.fetchone()
        data = {'nombre': usr[0], 'usuario': usr[1], 'cedula': usr[2], 'email': usr[3], 'direccion': usr[4], 'pais': usr[5], 'foto': usr[6], 'tipo': usr[7], 'id': usr[8]}
        

        if id == None:
            cur.execute("SELECT t.descripcion FROM tbl_redessociales t WHERE t.usr_id=%s", (session['id'],))
        else:
            cur.execute("SELECT t.descripcion FROM tbl_redessociales t WHERE t.usr_id=%s", (id,))
        rows = cur.fetchall()
        redes = []
        if cur.rowcount != 0 :
            for red in rows:
                redes.append({'descripcion':red[0]})
            
        return render_template('views/usuario.html', data=data, redes = redes,len = len(redes))

    except Exception as e:
        print(e)
        res = 'Ha ocurrido un error'
        return res
    finally:
        cur.close()

#Permite editar el perfil de un usuario
@app.route('/editar_usuario', methods=['GET', 'POST'])
def editUsuario():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if not 'usuario' in session:
            return redirect('/login')

        else:
            if request.method == 'GET':
                cur.execute("SELECT t.nombre, t.usuario, t.cedula, t.email, t.direccion, t.id_pais, t.foto, t.tipo_usuario, t.id_usr, t.password FROM tbl_usuarios t  WHERE t.id_usr=%s", (session['id'],))
                usr = cur.fetchone()
                item = {'nombre': usr[0], 'usuario': usr[1], 'cedula': usr[2], 'email': usr[3], 'direccion': usr[4], 'pais': usr[5], 'foto': usr[6], 'tipo': usr[7], 'id': usr[8], 'password':usr[9]}

                return render_template('views/editar_usuario.html', item=item)
            elif request.method == 'POST':
                data = request.form
                print(data)
                _nombre = data['nombre']
                _cedula = data['cedula']
                _email = data['email']
                _direccion = data['direccion']
                _pais = data['pais']

                if request.files['foto']:
                    f = request.files['foto']
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    _foto = f.filename

                    query = "UPDATE tbl_usuarios SET nombre = %s, cedula = %s, email = %s, direccion = %s, id_pais = %s, foto = %s WHERE id_usr = %s"
                    values = (_nombre, _cedula, _email, _direccion, _pais, _foto, session['id'],)
                    
                else:
                    query = "UPDATE tbl_usuarios SET nombre = %s, cedula = %s, email = %s, direccion = %s, id_pais = %s WHERE id_usr = %s"
                    values = (_nombre, _cedula, _email, _direccion, _pais, session['id'],)
                cur.execute(query, values)
                conn.commit()
                
                if session['tipo_usuario'] is 'T':

                    return redirect('/tienda')
                else:
                    return redirect('/perfil')

    except Exception as e:
        print(e)
        return redirect('/perfil')
    finally:
        cur.close()

#Esto no se implemento
@app.route('/ruleta')
def ruleta():
    try:
        return render_template('views/ruleta.html')
    except Exception as e:
        print(e)

#Lista de deseos via API del usuario
@app.route('/lista_deseos_api/<int:id>', methods=['POST', 'GET'])
def deseos(id = None):
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if not 'usuario' in session:
            return jsonify('Es necesario loguearse')
        else:
            _id_producto = id
            res = ''
            if request.method == 'POST':
                _json = request.get_json(force=True)
                 
                if _json['agregar'] == 'T':
                    cur.execute("INSERT INTO listadeseos (usr_id, id_producto) VALUES (%s, %s)", (session['id'], _id_producto))
                    conn.commit()
                    res = "Añadido a tu lista de deseos, se te notificaran sus cambios de ahora en adelante."
                elif _json['agregar'] == 'F':
                    cur.execute("DELETE FROM listadeseos WHERE usr_id = %s AND id_producto = %s", (session['id'], _id_producto))
                    conn.commit()
                    res = "Listo, dejaras de recibir notificaciones de este producto."

            elif request.method == 'GET':
                cur.execute("SELECT * FROM listadeseos WHERE usr_id = %s AND id_producto = %s", (session['id'], id))
                row = cur.fetchone()
                if row:
                    res = 'T'
                else:
                    res = 'F'

            return jsonify(res)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        
def aux():
    try:
        conn = mysql.connect()
        cur = conn.cursor()

    except Exception as e:
        print(e)
    finally:
        cur.close()