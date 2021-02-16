import os
# Secrets para randomizar el hex de las imagenes
import secrets
# Pillow para escalar las imagenes que ingresa el usuario
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# Funcion para que los usuarios suban una foto
def save_picture(form_picture):
	# Randomizamos el nombre de la imagen con un random hex de 8 bits
	random_hex = secrets.token_hex(12)
	# splittxt de os nos devuelve 2 atributos, el texto por un lado y la extension por el otro
	# file_name, file_extension = os.pathsplitext, _ se usa para declarar variables sin uso
	_, file_extension = os.path.splitext(form_picture.filename)
	picture_filename = random_hex + file_extension
	# Genero el path completo de la imagen con la extension
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
	
	# Vamos a reescalar la imagen que carga el usuario con Pillow (Image)
	output_size = (250, 250)
	i = Image.open(form_picture)
	# Escalo la imagen con la tupla donde le pasamos los pixels de salida
	i.thumbnail(output_size)

	# Grabo la imagen en el path que se arma apuntando a la carpeta prefile_pics escala a 125px
	i.save(picture_path)

	return picture_filename


# Metodo para envio de email con instrucciones de reseteo
def send_reset_email(user):
	token = user.get_reset_token()
	# Con _external le indicamos que es un domio full y no relativo a la aplicacion
	msg = Message('Solicitud para restablecer password', sender="demo@gmail.com", recipients=[user.email])
	msg.body = f'''
	Para restaurar tu password, ingresa al siguiente link: {url_for('users.reset_token', token=token, _external=True)}
	Si no solicitaste la restauracion de tu password simplemente ignora este mensaje y ningun cambio se realizada en el sistema.
	'''
	mail.send(msg)
