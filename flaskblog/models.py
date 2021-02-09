from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

# Uso el decorador y le asigno el cargador de usuarios 
# Tiene 4 atributos, isautenticated (credenciales validas), isactive, is anonimus, getid
@login_manager.user_loader
# Definimos una funcion para cargar un usuario
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref=db.backref('author', lazy=True)) # o lazy dynamic
	
	# Metodo para crear el token utilizando TimedJSONWebSignatureSerializer con un tiempo de 30 minutos(1800 segs)
	def get_reset_token(self, expires_sec=1800):
		# Creo una instancia del serializador utilizando la secret key de la aplicacion
		s = Serializer(app.config['SECRET_KEY'])
		# Creo el token con vencimiento pasandole por un diccionario el id del usuario (payload) y lo transformo de bits a utf-8
		return s.dumps({'user_id': self.id}).decode('utf-8')
	
	# Metodo statico que verifica si el token es valido
	# Se utiliza este decorador de estatico ya que no tiene que ver con el objeto en si no usamos self
	@staticmethod
	def verify_reset_token(token):
		# Creo un serializador con el secret key de la app
		s = Serializer(app.config['SECRET_KEY'])
		# Pruebo abrir el token y le pido el user_id del diccionario que se le paso cuando se creo el token  
		# Utilizo un try catch
		try:
			# Intento cargar el payload del token extrayendo el user_id
			user_id = s.loads(token)['user_id']
		except:
			return None
		# Si no salta la excepcion me devuelve el usuario con el id mandado por el diccionario 
		return User.query.get(user_id)

	def __repr__(self):
		#return f"Usuario: '{self.username} ({self.lastName}, {self.firstName})', '{self.email}', '{self.image_file}')"
		return f"Usuario: '{self.username})', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"