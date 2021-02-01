from flaskblog import app
# Esto permite correr el server sin necesidad de hacer "flask run" sino corriendo el script

if __name__ == '__main__':
	app.run(debug=True)