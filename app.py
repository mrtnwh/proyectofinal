from flask import Flask, render_template, request, redirect, url_for
import json, urllib.request

# API MOCKACHINO
response = ""

handlerApiUsuarios = urllib.request.urlopen("https://www.mockachino.com/e87585d1-9630-4f/usuarios")

for linea in handlerApiUsuarios:
    response += linea.decode()

listaUsuarios = json.loads(response)["usuarios"]

# FLASK
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()



