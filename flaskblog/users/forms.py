from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
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


# Formulario de la actualizacion del perfil
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

# Form de la pagina de solicitud de reseteo de la password
class RequestResetForm(FlaskForm):
	email = StringField('Correo Electronico (E-mail)', validators=[DataRequired(), Email()])
	submit = SubmitField('Resetear password')

	# Validacion similar al username pero con el email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError("No existe una cuenta con ese email")

# Form de reseteo de password
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Contraseña', validators=[DataRequired()])
	confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Cambiar password')