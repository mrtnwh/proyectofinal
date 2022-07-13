from datetime import datetime
from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import json, urllib.request, os

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

rutaPeliculas = 'static/json/peliculas.json'
rutaCriticas = 'static/json/criticas.json'

jsonPeliculas = getJson(rutaPeliculas)
listaPeliculas = jsonPeliculas["peliculas"]
jsonCriticas = getJson(rutaCriticas)

def dumpData(ruta, jsonData):
    with open(ruta, 'w') as file:
        json.dump(jsonData, file, ensure_ascii= False, indent=4)

# FLASK
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'C52zMh3cmKb5UvPg'
app.config['UPLOAD_FOLDER'] = 'static/img/posters_peliculas'

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
    listaFiltradas = [peli for peli in listaPeliculas if nombre == peli["director"]]

    return {"peliculas": listaFiltradas} 

@app.route("/portadas")
def peliculasConPortada():
    posterDefault = "https://i.ibb.co/5jXxMJ1/image-not-found.jpg"
    listaFiltradas = [peli for peli in listaPeliculas if posterDefault != peli["poster"]]
    
    return {"peliculas": listaFiltradas} 

def subir_poster():
    poster = request.files["poster"]
            
    if poster.filename == "":
        poster = "https://i.ibb.co/5jXxMJ1/image-not-found.jpg" 
    else:
        posterNombre = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], posterNombre))
        poster = app.config['UPLOAD_FOLDER'] + '/' + poster.filename

    return poster

@app.route("/subir_pelicula", methods=["POST", "GET"])
def subir_pelicula():

    if not session.get('logeado'):
        return render_template("login.html")
    else:

        if request.method == "POST":
            ultimoId = listaPeliculas[-1]["id"]

            posterLink = request.form["poster-link"]

            if posterLink != "":
                poster = posterLink
            else:
                poster = subir_poster()

            pelicula = {
                "id": ultimoId + 1,
                "title": request.form["title"],
                "director": request.form["director"],
                "date": request.form["date"],
                "poster": poster,
                "overview": request.form["overview"],
                "genre": request.form["genre"],
                "trailer": request.form["trailer"],
                "vote_average": 0,
                "vote_count": 0
            }

            listaPeliculas.append(pelicula)

            dumpData(rutaPeliculas, jsonPeliculas)

            return render_template("peliculas.html")

        return render_template("subir_pelicula.html")

@app.route("/peliculas")
def peliculas():
    return render_template("peliculas.html")

@app.route("/peliculas/<id>",  methods=["GET","DELETE"])
def pelicula_info(id):

    id = int(id)

    if request.method == "DELETE":
        if not session.get('logeado'):
            return render_template("login.html") 
        else:

            peliculaEncontrada = []
            sePuedeBorrar = True

            for elemPelicula in listaPeliculas:
                if id == elemPelicula["id"]:
                    peliculaEncontrada = elemPelicula
                    id = id

            for elemCritica in jsonCriticas["criticas"]:
                if id == elemCritica["id"]:
                    sePuedeBorrar = False
                    break
            
            if sePuedeBorrar:

                #Elimino el poster de la carpeta poster_peliculas
                if "https://i.ibb.co/5jXxMJ1/image-not-found.jpg" != peliculaEncontrada["poster"]:
                    print("entra al if para buscar el poster y borrarlo")
                    print(peliculaEncontrada["poster"])
                    os.remove(peliculaEncontrada["poster"])

                listaPeliculas.remove(elemPelicula)

                dumpData(rutaPeliculas, jsonPeliculas)

    return render_template("pelicula_info.html", id = id)

@app.route("/peliculas/<id>/editar",  methods=["GET","POST"])
def editarPelicula(id):

    pelicula = [peli for peli in listaPeliculas if id == str(peli["id"])]

    if request.method == "POST":

        poster = subir_poster()

        peliculaMod = {
                "id": int(id),
                "title": request.form["title"],
                "director": request.form["director"],
                "date": request.form["date"],
                "poster": poster,
                "overview": request.form["overview"],
                "genre": request.form["genre"],
                "trailer": request.form["trailer"],
                "vote_average": 0,
                "vote_count": 0
        }

        for index, elem in enumerate(listaPeliculas):
            if elem == pelicula[0]:
                listaPeliculas[index] = peliculaMod

        dumpData(rutaPeliculas, jsonPeliculas)
        
    pelicula = json.dumps(pelicula, ensure_ascii= False) #es necesario para convertir las comillas simples a dobles

    return render_template("editar_pelicula.html", pelicula = pelicula, id = id)


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

            dumpData(rutaCriticas, jsonCriticas)
            
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
    app.run()



