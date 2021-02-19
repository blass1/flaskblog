# __Proyecto Aplicación WEB FLASK BLOG__
## Documentado por Blas Carofile (bcarofile@gmail.com)
En mi pronta y joven carrera como desarrollador siempre fui un convencido que el conocimiento es muy complicado de transmitir, o eso pensaba hasta que encontré las herramientas indicadas. 
# MicroFramework FLASK (Como "DJANGO" pero más soft)
La escalabilidad de este framework esta siendo muy refinada por los programadores y logra un buen rendimiento (utilizando el patron de diseño correcto) y velocidad en el diseño e implementacion de sistemas web no muy amplios. Todo esto se logra con una gran abstrancion de lo que implicaria un diseño de backend mas profundo en lenguajes de mas bajo nivel. Las extensiones son maravillosas ya que nos resuelven muchas, muchas horas de programacion y ya estan testeadas y probadas por toda la comunidad. 

# Instalacion en linux (Ubuntu)
1) Crear VIRTUALENV
2) Instalar todas las dependencias automaticamente
~~~
pip install -r requirements.txt
~~~

# Correr el servidor de desarrollo en Linux (Ubuntu)
~~~
python3 run.py
~~~
# __Flask-Extensions (Resumen express del desarrollo)__

## __1- SQLAlchemy - El ORM que siempre quisiste tener.__
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

### Crear o borrar la BD
### Crear todas las tablas de la BD de SQLAlchemy
~~~
from flaskblog import db
db.create_all()
~~~
### Borrar la base de datos
~~~
db.drop_all()
~~~
### TEST SHELL Creacion de instancias de objetos USER y POST 
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
### Relaciones entre objetos de SQLAlchemy
Recorrer un lista de un query utilizando la relacion con otro objeto
~~~
for post in usuario1.posts:
     print(post.title)
~~~
Esto es posible porque en la clase User dentro de los modelos (models.py) declaramos la relationship con Post como el "author" de cada post.
~~~
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref=db.backref('author', lazy=True))

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"
~~~
### FILTRADO DE OBJETOS
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

## __2- WTFORMS + email_validator__
### Formularios para flask con validaciones

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
## __3- B-CRYPT__
Libreria para encryptar el password de los usuarios en nuestra base de datos
### Formularios con validaciones

### Instalación
~~~
pip3 install flask-bcrypt
~~~
### Importacion
~~~
from flask_bcrypt import Bcrypt
~~~
## Test practico de uso del b-crypt
### Creamos una instancia de clase Bcrypt
~~~
bcrypt = Bcrypt()
~~~
### Utilizamos el metodo que crea un password hash para la palabra 'blah' en binario
~~~
bcrypt.generate_password_hash('blah')
~~~
### Decodificamos a utf-8 el hash anterior y lo almaceno en una variable
~~~
hashed_pass = bcrypt.generate_password_hash('blah').decode('utf-8')
~~~
### Metodo que chequea que el hash generado con 'blah' sea compatible segundo argumento que se le pasa, como no es correcto devuelve __False__
~~~
bcrypt.check_password_hash(hashed_pass, 'hlab')
False
~~~
Si le enviamos el correcto devuelve True
~~~
bcrypt.check_password_hash(hashed_pass, 'blah')
True
~~~

## __4- FLASK LOGIN__
### Esta libreria sirve para manejar de manera simple las sesiones de usuario
## Instalacion
~~~
pip3 install flask_login
~~~

## __5- PILLOW__
### Esta libreria sirve para manejar imagenes, en nuestorr caso para reescalar la imagen que el usuario carga en su perfil
## Instalacion
~~~
pip3 install Pillow
~~~

## __6- FLASK MAIL__
### Maneja todo el envio de emails desde flask configurando la app
### Instalacion
~~~
pip3 install flask-mail
~~~

### Importar libreria (en el __init __.py)
~~~
from flask_mail import Mail
~~~

----
# __Paginacion__
La paginacion es la numeracion de cantidades configurables de objetos que se muestra por cada "página"  de objetos.

## Test de pagination
### Recorrer itinerando todos los objetos
~~~
from flaskblog.models import Post

posts = Post.query.all()

for post in posts:
     print(post)
~~~
### Crear objeto de tipo PAGINACION
~~~
posts = Post.query.paginate()
~~~

Utilizamos este metodo que muestra todos los metodos (valga la redundancia) de un objeto y vemos todo lo que tiene el paginador.
~~~
dir(posts)

'has_next', 'has_prev', 'items', 'iter_pages', 'next', 'next_num', 'page', 'pages', 'per_page', 'prev', 'prev_num', 'query', 'total']
~~~
### Metodo de paginacion que muestra cuantas paginas utiliza para paginar (por defecto son 20)
~~~
posts.per_page
20
~~~

### Mostrar porque pagina esta el paginador
~~~
posts.page
1
~~~
### Mostrar los objetos de la paginacion actual (1)
~~~
for post in posts.items:
	print(post)
~~~	
### Asignar al objeto de posts la pagina 2 de todos los registros del paginador	y la recorro
~~~	
posts = Post.query.paginate(page=2)
for post in posts.items:
     print(post)
~~~	
### Crear un objeto de paginacion con menos items
~~~
posts = Post.query.paginate(per_page=5)
~~~

### Creo una lista de posts que tenga 5 elementos por pagina y empieze en la 4
~~~
posts = Post.query.paginate(per_page=5, page=4)
~~~

### Mostrar total de objetos de la paginacion
~~~
posts.total
~~~

### METODO ITER_PAGES muestra kas paginas de la paginacion---
~~~
for page in posts.iter_pages():
    print(page)

... 
1
2
3
4
5
6
7
8
9
10
11
~~~

### De esta manera lo utilizamos en el BLOG pasandole por la url la pagina y ordenandolos segun su fecha de posteo
~~~
Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
~~~

# __Enviar valores al request por el navegador a Flask a travez de la URL__
Si quiero enviar a la pagina 3 del blog tengo que agregar "?page=3" a la ruta

http://127.0.0.1:5000/?page=3

# SIGNATURE USO DE SERIALIZADOR TimedJSONWebSignatureSerializer
## __Test de Serializador__
### Importo el paquete itsdangerous (que conjuntamente viene con la instalacion de flask)
~~~
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
~~~

### Creo una instancia del serializador y le asigno 30 segundos de expiracion
~~~
s = Serializer('secret', 30)
~~~
### Creo el token con expiracion de 30 segundos y le asigno el payload, el cual es un diccionario con el user_id. Decodificamos a utf-8 sino devuelve bits.
~~~
token = s.dumps({'user_id': 1}).decode('utf-8')
~~~
### Si utilizo el metodo loads del serializador(s) __antes de vencer__ nos devuelve el payload
~~~
s.loads(token)
~~~
~~~
{'user_id': 1}
~~~

### Si pasan los 30 segundos e intentamos hacer load del token nos muestra que la signature expiro
~~~
s.loads(token)
~~~
~~~
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/blaise/.local/lib/python3.8/site-packages/itsdangerous/jws.py", line 202, in loads
    raise SignatureExpired(
itsdangerous.exc.SignatureExpired: Signature expired
~~~

# __BLUEPRINTS__
### La base de un proyecto escalable es dividir el proyecto segun la funcion de cada modulo o aplicacion, ya que cuando tenes muchos forms y se va haciendo mas compleja la aplicacion es mejor separarla en blueprints 

1) Creo carpetas con los nombres de las funcionalidades de la aplicacion
users, posts, y main (paginas estaticas)

1) Agrego un __init __.py file en cada carpeta para que python sepa que son paquetes (no necesariamente tiene que tener algo)

2) Cada carpeta paquete tiene que tener su routes.py


### Esto es una ruta global de la app
~~~
@app.route('/register', methods=['GET', 'POST'])
def register():
...
~~~
### Si divido en blueprints la app, tengo que cambiar el decorador de las rutas segun el paquete que sea
~~~
@users.route('/register', methods=['GET', 'POST'])
def register():
...
~~~
