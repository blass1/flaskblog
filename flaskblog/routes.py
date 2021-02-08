import os
# Secrets para randomizar el hex de las imagenes
import secrets
# Pillow para escalar las imagenes que ingresa el usuario
from PIL import Image
# URL_FOR se ocupa de la lectura de los statics, flash es para la validacion del submit
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# Con route manejamos las urls
@app.route('/')
@app.route('/home')
def home():
	#posts = Post.query.all()
	# Con este metodo de request "get" traemos el valor "page" que por defecto ponemos que sea 1 y nos aseguramos que sea int
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	# Le envio el html y el contido del posts
	return render_template('home.html', posts=posts)


# Puede tener 2 decoradores route e ir la misma pagina
@app.route('/about')
def about():
	return render_template('about.html', title='Simplemente nosotros')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
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
		return redirect(url_for('login'))
	return render_template('register.html', title='Registro Blog de Blas', form=form)

# Con estos metodos envio informacion de la db a un form 
@app.route('/login', methods=['GET', 'POST'])
def login():
	# Utilizo otra funcion de flask_login que verifica si hay un usuario logueado
	if current_user.is_authenticated:
		return redirect(url_for('home'))
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
			return redirect(next_page) if next_page else redirect(url_for('home'))	
		else:
			flash('Login incorrecto. Revisa tu email y password e intenta nuevamente', 'danger')
	return render_template('login.html', title='Ingresa a la plataforma', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

# Funcion para que los usuarios suban una foto
def save_picture(form_picture):
	# Randomizamos el nombre de la imagen con un random hex de 8 bits
	random_hex = secrets.token_hex(12)
	# splittxt de os nos devuelve 2 atributos, el texto por un lado y la extension por el otro
	# file_name, file_extension = os.pathsplitext, _ se usa para declarar variables sin uso
	_, file_extension = os.path.splitext(form_picture.filename)
	picture_filename = random_hex + file_extension
	# Genero el path completo de la imagen con la extension
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
	
	# Vamos a reescalar la imagen que carga el usuario con Pillow (Image)
	output_size = (250, 250)
	i = Image.open(form_picture)
	# Escalo la imagen con la tupla donde le pasamos los pixels de salida
	i.thumbnail(output_size)

	# Grabo la imagen en el path que se arma apuntando a la carpeta prefile_pics escala a 125px
	i.save(picture_path)

	return picture_filename


@app.route('/account', methods=['GET', 'POST'])
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
		redirect(url_for('account'))
	# Cuando entre al accout se van a cargar los datos del usuario actual
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='/profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)

# Crear un post nuevo
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post (title=form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Tu post fue creado con exito!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='Nuevo Post', form=form,legend='Actualizar Post')

# Con esta ruta entramos a un posteo
# con el "int:" me aseguro que sea un entero
@app.route("/post/<int:post_id>")
def post(post_id):
	# Busca el post si no existe tira un 404
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

# Actualizar un posteo
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		# El error 403 es el que no permite acceder a una pagina
		abort(403)
	form = PostForm()
	# Si actualiza el post se manda el contenido de los form al objeto post
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		# No hace falta poner un add ya que el valor ya se encuentra en la base de datos
		db.session.commit()
		flash('Tu post fue actualizado con exito!', 'success')
		return redirect(url_for('post', post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Actualizar Post', form=form,legend='Actualizar Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		# El error 403 es el que no permite acceder a una pagina
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Tu post fue borrado!', 'danger')
	return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
	# Utilizo la pagina enviada por get
	page = request.args.get('page', 1, type=int)
	# Busco el usuario o tiro un error 404
	user = User.query.filter_by(username=username).first_or_404()
	# Almaceno la query con los posts del usuario, con \ sigo abajo
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	# Le envio el html y el contido del posts
	return render_template('user_posts.html', posts=posts, user=user)