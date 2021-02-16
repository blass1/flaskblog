from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# Instancio un blueprint del usuario
posts = Blueprint('posts', __name__)

# Crear un post nuevo
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post (title=form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Tu post fue creado con exito!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='Nuevo Post', form=form,legend='Actualizar Post')

# Con esta ruta entramos a un posteo
# con el "int:" me aseguro que sea un entero
@posts.route("/post/<int:post_id>")
def post(post_id):
	# Busca el post si no existe tira un 404
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

# Actualizar un posteo
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
		return redirect(url_for('posts.post', post_id = post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Actualizar Post', form=form,legend='Actualizar Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		# El error 403 es el que no permite acceder a una pagina
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Tu post fue borrado!', 'danger')
	return redirect(url_for('main.home'))