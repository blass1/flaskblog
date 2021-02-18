# Proyecto Aplicación WEB-BLOG - por Blas Carofile
En mi pronta y joven carrera como desarrollador siempre fui un convencido que el conocimiento es muy complicado de transmitir, o eso pensaba hasta que encontré las herramientas indicadas. 
# MicroFramework FLASK (Como "DJANGO" pero más soft)
La escalabilidad de este framework esta siendo muy refinada por los programadores y logra un buen rendimiento (utilizando el patron de diseño correcto) y velocidad en el diseño e implementacion de sistemas web no muy amplios. Todo esto se logra con una gran abstrancion de lo que implicaria un diseño de backend mas profundo en lenguajes de mas bajo nivel. Las extensiones son maravillosas ya que nos resuelven muchas, muchas horas de programacion y ya estan testeadas y probadas por toda la comunidad. 

# Instalacion en linux (Ubuntu)
1) Crear VIRTUALENV
2) Instalar todas las dependencias automaticamente
~~~
ip install -r requirements.txt
~~~

# Correr el servidor de desarrllo en Linux (Ubuntu)
~~~
python3 run.py
~~~
# Flask-Extensions (Resumen express del desarrollo)
__Al igual que en DJANGO, ya tenemos resuelto el tema de las sesiones, validaciones, almacenado de datos, etc..__

## 1) SQLAlquemy 
### Esta libreria sirve para interactuar con los datos de la BD como si se tratara de objetos de Python (SQL quíen te conoce)
### Instalación
~~~
pip3 install -U Flask-SQLAlchemy
~~~
### Instanciacion en el __init __.py de la aplicacion
~~~
from flask_sqlalchemy import SQLAlchemy
~~~
~~~
db = SQLAlchemy()
~~~
### Inicializamos la app en  __create_app()__ que se ejecutara posteriormente en el run.py
~~~
db.init_app(app)
~~~
### Ejemplo de utilizacion en la aplicacion (validación de usuario)
~~~
user = User.query.filter_by(username=username.data).first()
if user:
    raise ValidationError("Ese usuario ya existe, pruebe con otro distinto")
~~~
  
## 2) WTFORMS + email_validator
### Formularios con validaciones 

### Instalación
~~~
pip3 install flask-wtf
~~~
~~~
pip3 install email_validator
~~~
### Instanciación en forms.py de cada seccion de la aplicacion
~~~
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
~~~
### Ejemplo de uso en los forms
~~~
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Contraseña', validators=[DataRequired()])
	remember = BooleanField('Recuérdame')
	submit = SubmitField('Ingresar Ahora')
~~~


# SHELL usando SQLAlchemy
### Crear todas las tablas de la BD de SQLAlchemy
~~~
from flaskblog import db
db.create_all()
~~~
Crear instancias de objetos USER y POST 
~~~
from flaskblog import User, Post
~~~
~~~
user_1 = User(username='Ale', email='ale@gmail.com', password='password')
db.session.add(user_1)
user_2 = User(username='Blas', email='bla@gmail.com', password='password')
db.session.add(user_2)
db.session.commit()
~~~
~~~
post_1 = Post(title='Blog 111', content='Este es el primer contenido', user_id=user_1.id)
post_2 = Post(title='Blog 222', content='Este es el segundo contenido', user_id=user_2.id)
db.session.add(post_1)
db.session.add(post_2)
db.session.commit()
~~~
## FILTRADO DE OBJETOS
Crear un objeto que contenga TODOS los registros de su tipo que se pueden itinerar
~~~
todos = User.query.all()
~~~
Mostrar el primero
~~~
primeruser = User.query.first()
~~~
Lista [] de objetos filtrados por un objeto por un determinado campo
~~~
filtrados = User.query.filter_by(username='Ale').all()
~~~
Filtrar un usuario por un campo, devuelve un solo objeto.
~~~
primerofiltrado = User.query.filter_by(username='Ale').first()
~~~

Leer un atributo de un objeto
~~~
user.id
~~~
Traer objeto con su id
~~~
user = User.query.get(1)
~~~



# Carpetas (TREE)
