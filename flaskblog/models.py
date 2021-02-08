from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager
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