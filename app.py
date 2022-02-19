from distutils.log import debug
from flask import Flask, render_template, request
import json, urllib.request

# API MOCKACHINO
api = "https://www.mockachino.com/e87585d1-9630-4f"

def getResponse(api, endpoint='/'):
    handler = urllib.request.urlopen(api + endpoint)
    response = ''

    for linea in handler:
        response += linea.decode()

    return json.loads(response)

def getJsonPeliculas():
    with open('json/peliculas.json', 'r') as file:
        data = json.load(file)
        return data

data = getJsonPeliculas()

# FLASK
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    listaUsuarios = getResponse(api, "/usuarios")["usuarios"]

    if request.method == "POST":
        for usr in listaUsuarios:
            if request.form["email"] == usr["email"]:
                if request.form["password"] == usr["password"]:
                    return render_template("index.html")
    
    return render_template("login.html")

@app.route("/directores")
def getDirectores():
    return getResponse(api, "/directores")

@app.route("/generos")
def getGeneros():
    return getResponse(api, "/generos")

@app.route("/directores/<nombre>")
def peliculasXDirector(nombre):

    listaFiltradas = list()

    for pelicula in data["peliculas"]:
        if nombre == pelicula["director"]:
            listaFiltradas.append(pelicula)

    return {"peliculas": listaFiltradas}

@app.route("/portadas")
def peliculasConPortada():

    listaFiltradas = list()

    for pelicula in data["peliculas"]:
        if pelicula["poster"] != "":
            listaFiltradas.append(pelicula)
    
    return {"peliculas": listaFiltradas}

@app.route("/subir_pelicula", methods=["POST", "GET"])
def subir_pelicula():

    if request.method == "POST":
        ultimoId = data["peliculas"][-1]["id"]

        pelicula = {
            "id": ultimoId + 1,
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
            "vote_average": 0,
            "vote_count": 0
        }

        data["peliculas"].append(pelicula)

        with open('json/peliculas.json', 'w') as file:
            json.dump(data, file, indent=4)

        return render_template("index.html")

    return render_template("subir_pelicula.html")

if __name__ == "__main__":
    app.run(debug=True)



