from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flaskblog.models import User

# Creacion de un post nuevo
class PostForm(FlaskForm):
	title = StringField('Titulo', validators=[DataRequired()])
	content = TextAreaField('Contenido', validators=[DataRequired()])
	submit = SubmitField('Postear')