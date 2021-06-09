from flask import Flask
from flask_cors import CORS 
from flaskext.mysql import MySQL
from flask_session import Session

app = Flask(__name__, template_folder='templates')
CORS(app)

mysql = MySQL() # MySQL configurations 
app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = 'root' 
app.config['MYSQL_DATABASE_DB'] = 'bd_marketplace' 
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
mysql.init_app(app)

#Sesiones
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['UPLOAD_FOLDER'] = './pics'
#Fotos
# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']

#vistas 
import index
import auth
import user
import metodo_pago
import direccion_envio
