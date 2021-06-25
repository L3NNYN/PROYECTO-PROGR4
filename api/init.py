from flask import Flask, session
from flask_cors import CORS 
from flaskext.mysql import MySQL
from flask_session import Session

app = Flask(__name__, template_folder='templates')
CORS(app)

#Sesiones
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql = MySQL() # MySQL configurations 
app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = 'root' 
app.config['MYSQL_DATABASE_DB'] = 'bd_marketplace' 
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
mysql.init_app(app)

app.config['UPLOAD_FOLDER'] = './static/pics'
#Fotos
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']

 
#vistas
import controllers.index
import controllers.carrito
import controllers.auth
import controllers.user
import controllers.metodo_pago
import controllers.direccion_envio
import controllers.producto
import controllers.inicio
import controllers.redes_sociales
import controllers.tienda
import controllers.reportes
import controllers.calificacion
