from flaskblog.models import User, Post
from flaskblog import db

def postCreator():
    cantidadPosts = 10
    while cantidadPosts <= 0:
        usuario = User.query.get(2)
        titulo = "En este lugar va el titulo del post nro: " + str(cantidadPosts)
        contenidoGenerico = f"({cantidadPosts})Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico Contenido generico "
        post = Post(title=titulo, content=contenidoGenerico, user_id=usuario.id)
        db.session.add(post)
        cantidadPosts -= 1
    db.session.commit()

postCreator()