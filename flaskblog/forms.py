# Desde este archivo vamos a manejar los formularios de la aplicacion
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	# Tiene las validaciones de carga de datos preconfiguradas por wtforms	
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Correo Electronico (E-mail)', validators=[DataRequired(), Email()])
	password = PasswordField('Contraseña', validators=[DataRequired()])
	confirmPassword = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
	
	submit = SubmitField('Registrarse')

	# Para verificar que no existe un usuario con igual nombre
	def validate_username(self, username):
		# Creo una instancia de user y le asigno la data del campo username que escribio el usuario
		user = User.query.filter_by(username=username.data).first()
		# Si es verdadero quiere decir que ya existe en la db y le muestro un error.
		if user:
			raise ValidationError("Ese usuario ya existe, prueba con otro distinto")
	
	# Validacion similar al username pero con el email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Ese correo electronico ya posee una cuenta en nuestro sistema, pruebe con otro.")


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Contraseña', validators=[DataRequired()])
	remember = BooleanField('Recuérdame')
	submit = SubmitField('Ingresar Ahora')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Correo Electronico (E-mail)', validators=[DataRequired(), Email()])
	picture = FileField('Actualizar imagen de perfil', validators=[FileAllowed(['jpg', 'png'])])

	submit = SubmitField('Actualizar tus datos')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			# Si es verdadero quiere decir que ya existe en la db y le muestro un error.
			if user:
				raise ValidationError("Ese usuario ya existe, prueba con otro distinto")
	
	# Validacion similar al username pero con el email
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("Ese correo electronico ya posee una cuenta en nuestro sistema, pruebe con otro.")

class PostForm(FlaskForm):
	title = StringField('Titulo', validators=[DataRequired()])
	content = TextAreaField('Contenido', validators=[DataRequired()])
	submit = SubmitField('Postear')