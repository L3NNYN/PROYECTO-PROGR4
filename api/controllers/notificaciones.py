from flask import jsonify, request, render_template, redirect, session
from init import mysql
from init import app

@app.route('/notificaciones')
def notificaciones():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        if 'usuario' in session:
            return render_template('views/notificaciones.html')
        else:
            return redirect('/login')

    except Exception as e:
        print(e)
    finally:
        cur.close()

@app.route('/notificaciones_api', methods=['GET', 'DELETE'])
def notificacionesAPI():
    try:
        conn = mysql.connect()
        cur = conn.cursor()

        if not 'usuario' in session:
            return jsonify('Debes iniciar sesion')
        else:
            if request.method == 'GET':
                cur.execute("SELECT n.id_prod, p.descripcion, p.precio FROM notificaciones n LEFT JOIN tbl_productos p ON p.id_prod = n.id_prod WHERE n.visto = 'N' AND n.id_usr = %s", (session['id'], ))
                rows = cur.fetchall()
                notificaciones = []
                if rows != None:
                    for row in rows:
                        notificaciones.append({'id':row[0],'descripcion':row[1], 'precio': row[2]})
            
                return jsonify(notificaciones)
            elif request.method == 'DELETE':
                cur.execute("DELETE FROM notificaciones WHERE id_usr = %s", (session['id'], ))
                conn.commit()

                return jsonify('Te avisaremos cuando tengas notificaciones nuevas')

    except Exception as e:
        print(e)
    finally:
        cur.close()