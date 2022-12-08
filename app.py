import webbrowser
from datetime import datetime
from http import HTTPStatus
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json, urllib.request

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

# JWT
app.config["JWT_SECRET_KEY"] = 'dxM4-BL1CPeHYIMmXNQevdlsvhI'
jwt = JWTManager(app)

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

    pelicula = json.dumps(pelicula, ensure_ascii= False) #es necesario para convertir las comillas simples a dobles

    return render_template("editar_pelicula.html", pelicula = pelicula)

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
    webbrowser.open("https://documenter.getpostman.com/view/17933955/2s8YzP14aB")
    return redirect(url_for("index"))

@app.route("/api/directores")
def retornar_directores():
    return get_response(api_mocka, "/directores")

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
            token = create_access_token(identity=usr["user"])
            return jsonify({"token": token}), HTTPStatus.OK
            
    return jsonify({"status": 401, "message":"Error de validacion."}), HTTPStatus.UNAUTHORIZED

#PELICULAS
    #GET
@app.route("/api/peliculas")
def retornar_peliculas():
    return jsonify(listaPeliculas)

    #get peli info
@app.route("/api/peliculas/<id>")
def retornar_pelicula_info(id):
    pelicula = [peli for peli in listaPeliculas if id == str(peli["id"])]

    if pelicula == []:
        return jsonify({ "status": 404, "message": "Pelicula no encontrada"}), HTTPStatus.NOT_FOUND
    
    return jsonify(pelicula[0]), HTTPStatus.OK


def asignarPoster(poster):
    if poster == "":
        poster = "https://i.ibb.co/5jXxMJ1/image-not-found.jpg"
    
    return poster

    #POST
@app.route("/api/peliculas", methods=['POST'])
@jwt_required()
def api_subir_pelicula():
    data = request.get_json()
    ultimoId = listaPeliculas[-1]["id"]

    poster = asignarPoster(data["poster"])

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

    return jsonify(pelicula), HTTPStatus.CREATED


    #PUT
@app.route("/api/peliculas/<id>", methods=['PUT'])
@jwt_required()
def api_editar_pelicula(id):

    id = int(id)
    data = request.get_json()

    pelicula = [peli for peli in listaPeliculas if id == peli["id"]]

    if pelicula == []:
        return jsonify({ "status": 404, "message": "Pelicula no encontrada"}), HTTPStatus.NOT_FOUND

    poster = asignarPoster(data["poster"])

    peliculaMod = {
        "id": id,
        "title": data["title"],
        "director": data["director"],
        "date": data["date"],
        "poster": poster,
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

    return jsonify(peliculaMod), HTTPStatus.OK


    #DELETE
@app.route("/api/peliculas/<id>",  methods=["DELETE"])
@jwt_required()
def borrar_pelicula(id):
    id = int(id)
    sePuedeBorrar = True

    pelicula = [peli for peli in listaPeliculas if id == peli["id"]]

    if pelicula == []:
        return jsonify({ "status": 404, "message": "Pelicula no encontrada"}), HTTPStatus.NOT_FOUND

    for elemCritica in jsonCriticas["criticas"]:
        if id == elemCritica["id"]:
            sePuedeBorrar = False
            break
                
    if sePuedeBorrar:
        listaPeliculas.remove(pelicula[0])
        dump_data(rutaPeliculas, jsonPeliculas)

        return jsonify({ "status": 200, "message": "Pelicula borrada exitosamente"}), HTTPStatus.OK

    return jsonify({"status": 403, "message": "No se puede borrar. Hay criticas de usuarios."}), HTTPStatus.FORBIDDEN


@app.route("/api/peliculas/<id>/subir_critica" , methods=["POST"])
@jwt_required()
def api_subir_critica(id):

    id = int(id)

    data = request.get_json()
    dia = datetime.today().strftime('%d-%m-%Y')

    dictPelicula = {
        "id": id,
        "reviews": []
    } 

    dictCritica = {
        "user": get_jwt_identity(),
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

    return jsonify(dictCritica), HTTPStatus.CREATED       


if __name__ == "__main__":
    app.run(debug=True)



