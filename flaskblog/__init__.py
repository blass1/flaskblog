# Archivo necesario para que flaskblog se comporte como un paquete1
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a55c2258a11f94546c36492fde583725'
# Path de la BD,/// significa que es el relative path, de esta manera la busca en el directorio del proyecto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Instanciamos la base de datos de sqlalchemy
db = SQLAlchemy(app)
# Instalnciamos el encypter y le asignamos la app
bcrypt = Bcrypt(app)
# Vinculamos la libreria flask login a la app
login_manager = LoginManager(app)
# Tiene que ver con el login_required
login_manager.login_view = 'login'
# Con esto le mandamos un colorcito azul al boostrap como sen;al visual que ingreso
login_manager.login_message_category = 'info'

from flaskblog import routes
