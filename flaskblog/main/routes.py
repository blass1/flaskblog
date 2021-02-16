from flask import render_template, request, Blueprint
from flaskblog.models import Post

# Instancio un blueprint del usuario, esto se hace cuando divido la aplicacion en secciones
main = Blueprint('main', __name__)


# Con route manejamos las urls
@main.route('/')
@main.route('/home')
def home():
	#posts = Post.query.all()
	# Con este metodo de request "get" traemos el valor "page" que por defecto ponemos que sea 1 y nos aseguramos que sea int
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	# Le envio el html y el contido del posts
	return render_template('home.html', posts=posts)


# Puede tener 2 decoradores route e ir la misma pagina
@main.route('/about')
def about():
	return render_template('about.html', title='Simplemente nosotros')