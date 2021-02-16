from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# Instanciamos la base de datos de sqlalchemy y la vinculamos a la app
db = SQLAlchemy()
# Instanciamos el encypter y la vinculamos a la app
bcrypt = Bcrypt()
# Libreria flask login
login_manager = LoginManager()
# Cuando se le solicita el "login" se redicciona al blueprint de usuarios
login_manager.login_view = 'users.login'
# Con esto le mandamos un colorcito azul al boostrap como senial visual que ingreso
login_manager.login_message_category = 'info'

mail = Mail()

# Cuando no usamos blueprints importabamos las rutas de aca
#from flaskblog import routes

# Con este patron de diseno en donde las extensiones se instancian primero y luego la app
def create_app(config_class=Config):
    app = Flask(__name__)
    # Le seteamos la configuracion a la apliacaion de nuestro archivo config.py
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Importo el blueprint de users, posts y del main
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    # Se agregan los blueprints a la app
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app