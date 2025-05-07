from flask import Flask, render_template, session, redirect, url_for, request
from .model.bdd import verifAuthData


from .viewsthomas import view2


app = Flask(__name__)   
view2(app)
app.template_folder = "template"
app.static_folder = "static"
app.config.from_object('myApp.config')

@app.route("/")
def index():
       return render_template("index.html")

@app.route("/index")
def ind():
       return redirect(url_for("index"))

@app.route("/A_propos")
def propos():
       return render_template("A_propos.html")

@app.route('/login', methods=['POST']) 
def login():


       username = request.form['username']  
       password = request.form['password']  
       user = verifAuthData(username, password)

       print(f"Username: {username}, Password: {password}, Work : {user}")
       try:
              # Authentification réussie
              session["idUser"] = user["idUser"]
              session["nom"] = user["nom"]
              session["prenom"] = user["prenom"]
              session["mail"] = user["mail"]
              session["statut"] = user["statut"]
              session["avatar"] = user["avatar"]
              session["infoVert"]="Authentification réussie"
              return redirect("/")
       except TypeError as err:
              # Authentification refusée
              session["infoRouge"]="Authentification refusée"
              return redirect("/login")

@app.route("/login")
def loginfonction():
       return render_template("login.html")

@app.route("/register")
def ccfonction():
       return render_template("creation_compte.html")