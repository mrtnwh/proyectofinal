from distutils.log import debug
from flask import Flask, render_template, request, session
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
    with open('static/json/peliculas.json', 'r') as file:
        data = json.load(file)
        return data

data = getJsonPeliculas()

# FLASK
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'C52zMh3cmKb5UvPg'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    listaUsuarios = getResponse(api, "/usuarios")["usuarios"]

    if request.method == "POST":
        for usr in listaUsuarios:
            if request.form["email"] == usr["email"] and request.form["password"] == usr["password"]:
                session['logeado'] = True
                return render_template("index.html")
    
    return render_template("login.html")

@app.route("/directores")
def getDirectores():
    return getResponse(api, "/directores")

@app.route("/get-generos")
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

    if not session.get('logeado'):
        return render_template("login.html")
    else:

        if request.method == "POST":
            ultimoId = data["peliculas"][-1]["id"]

            if request.form["poster"] == "" :
                poster = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png"
            else:
                poster = request.form["poster"]

            pelicula = {
                "id": ultimoId + 1,
                "title": request.form["title"],
                "director": request.form["director"],
                "date": request.form["date"],
                "poster": poster,
                "overview": request.form["overview"],
                "genre": request.form["genre"],
                "vote_average": 0,
                "vote_count": 0
            }

            data["peliculas"].append(pelicula)

            with open('static/json/peliculas.json', 'w') as file:
                json.dump(data, file, indent=4)

            return render_template("peliculas.html")

        return render_template("subir_pelicula.html")

@app.route("/peliculas")
def peliculas():
    return render_template("peliculas.html")

@app.route("/peliculas/<id>")
def pelicula(id):
    return render_template("pelicula_info.html", id = id)

@app.route("/generos")
def generos():
    return render_template("generos.html")

@app.route("/generos/<genero>")
def peliPorGenero(genero):
    genero = genero.capitalize()

    if genero == "Ciencia%20ficcion":
        genero = "Ciencia ficcion"

    return render_template("peliculas_genero.html", genero = genero)

if __name__ == "__main__":
    app.run(debug=True)



