from flask import jsonify, request, render_template, redirect, session
from init import app

@app.route('/')
def render():
    return render_template("views/index.html")

@app.route('/tienda', methods=['GET'])
def tienda(name = None):
    name = ['hola', 'hi', 'heo']
    return render_template("views/tienda.html", len = len(name), name = name)

@app.route('/inicio')
def inicio():
    return render_template("views/inicio.html")