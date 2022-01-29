from flask import Flask, jsonify, render_template, request
import json, urllib.request

# API MOCKACHINO

    #Usuarios
handlerApiUsuarios = urllib.request.urlopen("https://www.mockachino.com/e87585d1-9630-4f/usuarios")
response = ''

for linea in handlerApiUsuarios:    # OPTIMIZAR
    response += linea.decode()

listaUsuarios = json.loads(response)["usuarios"]

# FLASK
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        for usr in listaUsuarios:
            if email == usr["email"]:
                if password == usr["password"]:
                    return render_template("index.html")
    
    return render_template("login.html")

@app.route("/directores")
def getDirectores():
    response = ''
    handler = urllib.request.urlopen("https://www.mockachino.com/e87585d1-9630-4f/directores")
    
    for linea in handler:
        response += linea.decode()

    return json.loads(response)

@app.route("/generos")
def getGeneros():
    response = ''
    handler = urllib.request.urlopen("https://www.mockachino.com/e87585d1-9630-4f/generos")
    
    for linea in handler:
        response += linea.decode()

    return json.loads(response)


""" @app.route("/subir_pelicula", methods=["POST", "GET"])
def subir_pelicula():
    if request.method == "POST":
        ultimoId = listaPeliculas[-1]['id']

        data = jsonify({
            "id": ultimoId, 
            "title": request.form["title"],
            "director": request.form["director"],
            "date": request.form["date"],
            "poster": request.form["poster"],
            "overview": request.form["overview"],
            "genre": [
                    {
                        "id":0,
                        "name": request.form["genre"]
                    }
            ],
        })
    else:
        return render_template("subir_pelicula.html")

    return render_template("subir_pelicula.html") """

if __name__ == "__main__":
    app.run()



