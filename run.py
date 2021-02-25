from flaskblog import create_app
# Esto permite correr el server sin necesidad de hacer "flask run" sino corriendo el script

app = create_app()

if __name__ == '__main__':
	#app.run(debug=True)
	app.run()