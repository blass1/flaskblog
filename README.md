# Proyecto de aplicacion web "Flaskblog"
## Instalacion en linux (Ubuntu)
Entrar en el entorno virtual donde vamos a instalar Flask y algunas librerias complementarias de python para que funcione.
* pip install -r requirements.txt

## Correr proyecto
El archivo run contiene la "app flask" y la configuracion del modo debug en True que nos muestra los errores que pueden ir apareciendo en el desarollo. Una vez que este concluida hay que desactivarlo para no dar informacion a alguien que intencionalmente quiera hackearla.
* python3 run.py

## Utilizar un modelo como objeto desde la consola de python
'''
Crear la base de datos
python3
from appfinanzas import db
db.create_all()
'''