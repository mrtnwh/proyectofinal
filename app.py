from datetime import datetime
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

# JSON
def getJson(url):
    with open(url, 'r') as file:
        data = json.load(file)
        return data

jsonPeliculas = getJson('static/json/peliculas.json')
listaPeliculas = jsonPeliculas["peliculas"]

jsonCriticas = getJson('static/json/criticas.json')


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
                session['user'] = request.form["email"]
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

    for pelicula in listaPeliculas:
        if nombre == pelicula["director"]:
            listaFiltradas.append(pelicula)

    return {"peliculas": listaFiltradas}

@app.route("/portadas")
def peliculasConPortada():

    listaFiltradas = list()

    for pelicula in listaPeliculas:
        if pelicula["poster"] != "":
            listaFiltradas.append(pelicula)
    
    return {"peliculas": listaFiltradas}

@app.route("/subir_pelicula", methods=["POST", "GET"])
def subir_pelicula():

    if not session.get('logeado'):
        return render_template("login.html")
    else:

        if request.method == "POST":
            ultimoId = listaPeliculas[-1]["id"]

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

            listaPeliculas.append(pelicula)

            with open('static/json/peliculas.json', 'w') as file:
                json.dump(jsonPeliculas, file, indent=4)

            return render_template("peliculas.html")

        return render_template("subir_pelicula.html")

@app.route("/peliculas")
def peliculas():
    return render_template("peliculas.html")

@app.route("/peliculas/<id>")
def pelicula(id):
    return render_template("pelicula_info.html", id = id)

@app.route("/peliculas/<id>/eliminar")
def eliminarPelicula(id):

    id = int(id)

    if not session.get('logeado'):
        return render_template("login.html")
    else:
        for elemCritica in jsonCriticas["criticas"]:
            if id == elemCritica["id"] and len(elemCritica["reviews"]) == 0:
                for elemPelicula in listaPeliculas:
                    if id == elemPelicula["id"]:
                        listaPeliculas.remove(elemPelicula)

                        # Hacer funcion, se repite mucho en el codigo
                        with open('static/json/peliculas.json', 'w') as file:
                            json.dump(jsonPeliculas, file, indent=4)

    return render_template("peliculas.html", id = id)

@app.route("/peliculas/<id>/subir_critica" , methods=["POST", "GET"])
def subir_critica(id):

    id = int(id)
    dia = datetime.today().strftime('%d-%m-%Y')
    listaUsuarios = getResponse(api, "/usuarios")["usuarios"]

    if not session.get('logeado'):
        return render_template("login.html") 
    else:
        if request.method == "POST":

            for usr in listaUsuarios:
                if session.get('user') == usr["email"]:
                    nombreUser = usr["user"]

            dictPelicula = {
                "id": id,
                "reviews": []
            } 

            dictCritica = {
                "user": nombreUser,
                "review_title": request.form["title"], 
                "review_text": request.form["review"],
                "date": dia
            }

            def agregarCritica():
                existePelicula = False
                for peli in jsonCriticas["criticas"]:
                    if id == peli["id"]:
                        peli["reviews"].append(dictCritica)
                        existePelicula = True
                        break
                return (jsonCriticas["criticas"], existePelicula)
            
            jsonCriticas["criticas"], existePelicula = agregarCritica()

            if existePelicula == False:
                jsonCriticas["criticas"].append(dictPelicula)
                agregarCritica()

            with open('static/json/criticas.json', 'w') as file:
                    json.dump(jsonCriticas, file, indent=4)
            
            return render_template("pelicula_info.html", id = id)

        return render_template("subir_critica.html", id = id)       

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



