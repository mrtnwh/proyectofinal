from datetime import datetime
from http import HTTPStatus
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import json, urllib.request, os

# API MOCKACHINO
api_mocka = "https://www.mockachino.com/e87585d1-9630-4f"

def get_response(api, endpoint='/'):
    handler = urllib.request.urlopen(api + endpoint)
    response = ''

    for linea in handler:
        response += linea.decode()

    return json.loads(response)

# JSON
def get_json(url):
    with open(url, 'r') as file:
        data = json.load(file)
        return data

rutaPeliculas = 'static/json/peliculas.json'
rutaCriticas = 'static/json/criticas.json'

jsonPeliculas = get_json(rutaPeliculas)
listaPeliculas = jsonPeliculas["peliculas"]
jsonCriticas = get_json(rutaCriticas)

def dump_data(ruta, jsonData):
    with open(ruta, 'w', encoding="utf-8") as file:
        json.dump(jsonData, file, ensure_ascii= False, indent=4)

# FLASK
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'C52zMh3cmKb5UvPg'
# TODO: Borrar??
app.config['UPLOAD_FOLDER'] = 'static/img/posters_peliculas'



# RENDERS
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/subir_pelicula")
def subir_pelicula():
    return render_template("subir_pelicula.html")

@app.route("/peliculas")
def peliculas():
    return render_template("peliculas.html")

@app.route("/peliculas/<id>")
def pelicula_info(id):
    return render_template("pelicula_info.html", id = id)

@app.route("/peliculas/<id>/editar")
def editar_pelicula(id):

    # Devuelvo la pelicula que se quiere editar para que el usuario vea su informacion actual
    pelicula = [peli for peli in listaPeliculas if id == str(peli["id"])]

    return render_template("editar_pelicula.html", pelicula = pelicula, id = id)

@app.route("/peliculas/<id>/subir_critica")
def subir_critica(id):
    return render_template("subir_critica.html", id = id)

@app.route("/generos")
def generos():
    return render_template("generos.html")

@app.route("/generos/<genero>")
def peli_por_genero(genero):
    genero = genero.capitalize()

    if genero == "Ciencia%20ficcion":
        genero = "Ciencia ficcion"

    return render_template("peliculas_genero.html", genero = genero)



#API
@app.route('/api')
def api():
    #TODO: Documentacion postman
    return redirect(url_for("index"))

@app.route("/api/directores")
def retornar_directores():
    return get_response(api_mocka, "/directores")

#TODO: Arreglar no reconoce el nombre por los espacios?
@app.route("/api/directores/<nombre>")  
def retornar_peli_por_director(nombre):
    listaFiltradas = [peli for peli in listaPeliculas if nombre == peli["director"]]

    return jsonify(listaFiltradas)

@app.route("/api/generos")
def retornar_generos():
    return get_response(api_mocka, "/generos")

@app.route("/api/generos/<genero>")
def retornar_peli_por_genero(genero):
    listaFiltradas = [peli for peli in listaPeliculas if genero.capitalize() == peli["genre"]]

    return jsonify(listaFiltradas)

@app.route("/api/portadas")
def retornar_peli_con_portada():
    posterDefault = "https://i.ibb.co/5jXxMJ1/image-not-found.jpg"
    listaFiltradas = [peli for peli in listaPeliculas if posterDefault != peli["poster"]]
    
    return jsonify(listaFiltradas)

@app.route("/api/criticas")
def retornar_criticas():
    return jsonify(jsonCriticas["criticas"])



#USUARIOS
@app.route("/api/usuarios")
def retornar_usuarios():
    return get_response(api_mocka, "/usuarios")

@app.route("/api/login", methods=["POST"])
def logearse():
    listaUsuarios = get_response(api_mocka, "/usuarios")["usuarios"]
    data = request.get_json() 

    for usr in listaUsuarios:
        if data["email"] == usr["email"] and data["password"] == usr["password"]:
            session['logeado'] = True
            session['user_name'] = usr["user"]
            return jsonify(usr), HTTPStatus.OK
            
    return jsonify("Error de validacion."), HTTPStatus.UNAUTHORIZED



#PELICULAS
    #GET
@app.route("/api/peliculas")
def retornar_peliculas():
    return jsonify(listaPeliculas)

    #get peli info
@app.route("/api/peliculas/<id>")
def retornar_pelicula_info(id):
    pelicula = [peli for peli in listaPeliculas if id == str(peli["id"])]
    
    return jsonify(pelicula)

    #POST
#TODO: Cuando se sube tiene que redireccionar a peliculas. ERROR 400 BAD REQUEST.
@app.route("/api/peliculas", methods=['POST'])
def api_subir_pelicula():
    data = request.get_json()

    if not session.get('logeado'):
        return redirect(url_for("login"))
    else:
        ultimoId = listaPeliculas[-1]["id"]

        posterLink = data["poster"]

        if posterLink != "":
            poster = posterLink
        else:
            poster = "https://i.ibb.co/5jXxMJ1/image-not-found.jpg"

        pelicula = {
            "id": ultimoId + 1,
            "title": data["title"],
            "director": data["director"],
            "date": data["date"],
            "poster": poster,
            "overview": data["overview"],
            "genre": data["genre"],
            "trailer": data["trailer"]
        }

        listaPeliculas.append(pelicula)
        dump_data(rutaPeliculas, jsonPeliculas)                                 

    return jsonify(pelicula), HTTPStatus.OK

#TODO: Borrar? creo que se borro la funcion de subir un poster desde pc
# Función Auxiliar
def subir_poster():
    poster = request.files["poster"]
            
    if poster.filename == "":
        poster = "https://i.ibb.co/5jXxMJ1/image-not-found.jpg" 
    else:
        posterNombre = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], posterNombre))
        poster = app.config['UPLOAD_FOLDER'] + '/' + poster.filename
    return poster


    #PUT
@app.route("/api/peliculas/<id>", methods=['PUT'])
def api_editar_pelicula(id):

    if not session.get('logeado'):
        return redirect(url_for("login"))
    else:
        data = request.get_json()

        pelicula = [peli for peli in listaPeliculas if id == str(peli["id"])]
        #poster = subir_poster()

        peliculaMod = {
            "id": int(id),
            "title": data["title"],
            "director": data["director"],
            "date": data["date"],
            "poster": data["poster"],
            "overview": data["overview"],
            "genre": data["genre"],
            "trailer": data["trailer"]
        }

        #Actualizo la informacion
        for index, elem in enumerate(listaPeliculas):
                if elem == pelicula[0]:
                    listaPeliculas[index] = peliculaMod
                    break

        dump_data(rutaPeliculas, jsonPeliculas)

    return jsonify(peliculaMod)

    #DELETE
@app.route("/api/peliculas/<id>",  methods=["DELETE"])
def borrar_pelicula(id):
    id = int(id)

    if not session.get('logeado'):
        return redirect(url_for("login"))
    else:
        peliculaEncontrada = []
        sePuedeBorrar = True

        for elemPelicula in listaPeliculas:
            if id == elemPelicula["id"]:
                peliculaEncontrada = elemPelicula
                id = id
                break

        for elemCritica in jsonCriticas["criticas"]:
            if id == elemCritica["id"]:
                sePuedeBorrar = False
                break
                
        if sePuedeBorrar:
            #TODO: Borrar carpeta img/poster_peliculas
            listaPeliculas.remove(peliculaEncontrada)
            dump_data(rutaPeliculas, jsonPeliculas)

            return jsonify("Pelicula borrada exitosamente."), HTTPStatus.OK

    return jsonify("No se puede borrar. Hay criticas de usuarios."), HTTPStatus.FORBIDDEN


@app.route("/api/peliculas/<id>/subir_critica" , methods=["POST"])
def api_subir_critica(id):

    data = request.get_json()
    id = int(id)
    dia = datetime.today().strftime('%d-%m-%Y')

    if not session.get('logeado'):
        print("hay que logearse")
        return url_for("login")
    else:
        dictPelicula = {
            "id": id,
            "reviews": []
        } 

        dictCritica = {
            "user": session.get('user_name'),
            "review_title": data["review_title"],  
            "review_text": data["review_text"],
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

        dump_data(rutaCriticas, jsonCriticas)

    return jsonify(dictCritica), HTTPStatus.OK       


if __name__ == "__main__":
    app.run()



