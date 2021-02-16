""" En este archivo vamos a poner todas las configuraciones de la app
Tambien podrian estar guardadas en el __init__.py 
Ejemplo: app.config['MAIL_PORT'] = 465
Es buena costumbre guardar la informacion sensible en variables de entorno utilizando os
"""
import os

class Config:
    #SECRET_KEY = 'a55c2258a11f94546c36492fde583725'
    SECRET_KEY =  os.environ.get('SECRET_KEY')
    # Path de la BD, /// significa que es el relative path, de esta manera la busca en el directorio del proyecto 
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # Configuracion de la libreria Flask Mail con Gmail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')