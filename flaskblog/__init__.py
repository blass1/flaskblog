import os
# Archivo necesario para que flaskblog se comporte como un paquete1
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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
# Con esto le mandamos un colorcito azul al boostrap como senial visual que ingreso
login_manager.login_message_category = 'info'

# Configuracion de Flask Mail con Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# Para las credenciales del email utilizo variables de entorno
#app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
#app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USERNAME'] = "blas.carofile@gmail.com"
app.config['MAIL_PASSWORD'] = "blass2547"

mail = Mail(app)

from flaskblog import routes
