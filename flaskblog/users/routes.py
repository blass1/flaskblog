from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
# Importo de un paquete dentro de otro flaskblog -> user -> forms
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

# Instancio un blueprint del usuario
users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		# Hasheamos el pass que el usuario pone en el campo password del formulario
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		# Creamos una nueva instancia del usuario
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		# Aniadiamos el usuario a la base de datos y commiteamos
		db.session.add(user)
		db.session.commit()
		# Flash messege en flask es una alerta que se manda al template, en este caso success "category"
		#'success' es la clase de boostrap
		flash(f'Tu cuenta ha sido creada con exito. Ahora puedes iniciar sesion', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Registro Blog de Blas', form=form)

# Con estos metodos envio informacion de la db a un form 
@users.route('/login', methods=['GET', 'POST'])
def login():
	# Utilizo otra funcion de flask_login que verifica si hay un usuario logueado lo mando al home
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	# Si se valida correctamente cuando envia los datos
	if form.validate_on_submit():
		# Cre una instancia de usuario y busco en la db al que tenga este email
		user = User.query.filter_by(email=form.email.data).first()
		# Si hay instancia de usuario y la comparacion entre el hash y la clave enviada a travez
		# del formulario en el campo password
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# Hago el login de sesion con el usuario y le paso el campo que mantiene la sesion abierta
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			# Mandame a la ruta de next page si next_page no es nulla o falsa sino mandame a home
			return redirect(next_page) if next_page else redirect(url_for('main.home'))	
		else:
			flash('Login incorrecto. Revisa tu email y password e intenta nuevamente', 'danger')
	return render_template('login.html', title='Ingresa a la plataforma', form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
# Con este decorador podes redirigir usuarios (al login) no autenticados que quieren entrar
@login_required
def account():
	form = UpdateAccountForm()
	# Si se valida la data se le asigna el valor del form al current y un commit para la db
	if form.validate_on_submit():
		# Chequeamos si el usuario puso una imagen para actualizar el perfil
		if form.picture.data:
			# Utilizo la funcion que creamos que asigna el nombre y devuelve la ruta
			picture_filename = save_picture(form.picture.data)
			# Asignamos a la ruta del usuario actual la ruta que creamos con a funcion
			current_user.image_file = picture_filename
		# Asignamos data al current user cuando el usuario modifica los campos
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Tu cuenta ha sido actualizada', 'success')
		redirect(url_for('users.account'))
	# Cuando entre al accout se van a cargar los datos del usuario actual
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='/profile_pics/' + current_user.image_file)
	return render_template('account.html', title=f'Perfil de {current_user.username}', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
	# Utilizo la pagina enviada por get
	page = request.args.get('page', 1, type=int)
	# Busco el usuario o tiro un error 404
	user = User.query.filter_by(username=username).first_or_404()
	# Almaceno la query con los posts del usuario, con \ sigo abajo
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	# Le envio el html y el contido del posts
	return render_template('user_posts.html', posts=posts, user=user)


# Reseteo de password, si esta logeado vuelve al home, sino carga el form del reseteo
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Un email fue enviado a tu direccion de correo con el instructivo de como resetear tu password', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Resetea tu password', form=form)


# Verificacion del token a travez de la url
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('Token invalido o expirado', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		# Hasheamos el pass que el usuario pone en el campo password del formulario
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Tu password se ha cambiado con exito. Ahora puedes iniciar sesion', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Resetea tu password', form=form)