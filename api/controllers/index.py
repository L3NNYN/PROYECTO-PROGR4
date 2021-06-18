from flask import jsonify, request, render_template, redirect, session, flash
from init import app
from init import mysql


@app.route('/')
def render():
    return render_template("views/index.html")

@app.route('/tienda', methods=['GET'])
def tienda():
    return render_template("views/tienda.html")

@app.route('/inicio')
def inicio():
    return render_template("views/inicio.html")

@app.route('/paises_api')
def paises():
    try:
        cur = mysql.connect().cursor()
        cur.execute("SELECT id_pais, descripcion FROM tbl_paises")
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