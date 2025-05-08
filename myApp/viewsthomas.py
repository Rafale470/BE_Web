from flask import Flask, render_template, session, redirect, url_for, request
import hashlib
from .model.bddthomas import add_membreData
from .model.bddthomas import get_membresData
from .model.bddthomas import del_membreData
from werkzeug.utils import secure_filename
import pandas, os
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/files/'

def view2(app) :
    @app.route("/register", methods=['POST'])
    def register():
        if request.form['password'] != request.form['password2'] :
            return redirect("/register")
        identifiant = request.form['identifiant']
        motPasse =hashlib.sha256(request.form['password'].encode())
        nom = request.form['nom']
        prenom = request.form['prenom']
        mail = request.form['mail']
        motPasse = motPasse.hexdigest() 
        lastId = add_membreData(identifiant, motPasse, nom, prenom, mail)
        return redirect("/index")

    @app.route("/test")
    def test():
        return render_template("index.html.jinja")

    @app.route("/sgbd")
    def sgbd():
        listeMembres = get_membresData()
        params ={
        'liste':listeMembres
        }
        #params = f.messageInfo(params)
        return render_template("sgbd.html.jinja", **params)
    
    @app.route("/suppMembre/<user_id>")
    def suppMembre(idUser=""):
        del_membreData(idUser)
        if "errorDB" not in session:
            session["infoVert"]="L'utilisateur a bien été supprimé"
        else:
            session["infoRouge"] = "Problème suppression utilisateur"
        return redirect("/sgbd")