import os
from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

@app.route('/perfil', methods=['GET', 'PUT'])
def pefil():
    try:
        # if !session['usuario']:
        #     return redirect('/index')
        cur = mysql.connect().cursor()
        
        if request.method == 'GET':
            cur.execute("SELECT t.nombre, t.usuario, t.cedula, t.email, t.direccion, t.id_pais, t.foto, t.tipo_usuario, t.password FROM tbl_usuarios t WHERE t.id_usr=%s", (session['id'],))
            usr = cur.fetchone()

            data = {'nombre': usr[0], 'usuario': usr[1], 'cedula': usr[2], 'email': usr[3], 'direccion': usr[4], 'pais': [5], 'foto': usr[6], 'password': usr[8]}

            return render_template('views/usuario.html', data =data)
        elif request.method == 'PUT':
            return redirect('/perfil')
    except Exception as e:
        print(e)
        res = 'Ha ocurrido un error'
        return res
    finally:
        cur.close()

@app.route('/ruleta')
def ruleta():
    try:
        return render_template('views/ruleta.html')
    except Exception as e:
        print(e)

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
                    res = "Añadido a tu lista de deseos correctamente, se te notificaran cambios en su precio y descripcion de ahora en adelante."
                elif _json['agregar'] == 'F':
                    cur.execute("DELETE FROM listadeseos WHERE usr_id = %s AND id_producto = %s", (session['id'], _id_producto))
                    conn.commit()
                    res = "Eliminado de tu lista de deseos, dejaras de recibir notificaciones de este producto."

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