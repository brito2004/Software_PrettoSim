from flask import Flask
from flask_mysqldb import MySQL
from .config import Config

app = Flask(__name__, template_folder='templates') 
app.config.from_object(Config)

# Inicializando MySQL
mysql = MySQL(app)

from .controllers import *  # Certifique-se de que os controladores estão sendo importados corretamente
