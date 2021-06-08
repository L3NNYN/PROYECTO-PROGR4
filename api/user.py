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

        print('asd')
    except Exception as e:
        print(e)
        res = 'Ha ocurrido un error'
        return res
    finally:
        cur.close()