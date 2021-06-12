from flask import jsonify, request, render_template, redirect, session, flash
from init import app
from init import mysql


@app.route('/')
def render():
    # session['auth'] = False
    # session['id'] = ''
    # session['usuario'] = ''
    # session['nombre'] = ''
    # session['tipo_usuario'] = ''
    if 'usuario' in session:
        print(session['usuario'])
        # return render_template("views/index.html")
        return redirect('/inicio')
    else:
        return render_template("views/index.html")


@app.route('/tienda', methods=['GET'])
def tienda():

    return render_template("views/tienda.html")

@app.route('/inicio')
def inicio():
    return render_template("views/inicio.html")

@app.route('/paises')
def paises():
    try:
        cur = mysql.connect().cursor()
        cur.execute("SELECT * FROM tbl_paises")
        rows = cur.fetchall()
        json_items = []
        content = {}
        for result in rows:
            content = {'value': result[0], 'text': result[1]} #value = id, text = nombre del pais
            json_items.append(content)
        content ={}
        return jsonify(json_items) #se retorna el formato JSON
    except Exception as e:
        print(e)
    finally:
        cur.close()
        print('listo')