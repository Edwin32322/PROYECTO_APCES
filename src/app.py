
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

#Creamos las instancias de los objetos que necesitemos
app = Flask(__name__)
login_manager = LoginManager(app)
csrf = CSRFProtect()