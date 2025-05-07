from flask import Flask, render_template, session, redirect, url_for, request
import hashlib
from .model.bddthomas import *

def view2(app) :
    @app.route("/register", methods=['POST'])
    def register():
        identifiant = request.form['identifiant']
        motPasse =request.form['password']
        motPasse2 = request.form['password2']
        nom = request.form['nom']
        prenom = request.form['prenom']
        mail = request.form['mail']
        lastId = add_membreData(identifiant, motPasse, nom, prenom, mail)
        print("dans addmembre")
        return redirect("/index")

    @app.route("/test")
    def test():
        return render_template("index.html")