from flask import Flask, render_template, session, redirect, url_for, request
import hashlib
from .model.bddthomas import add_membreData
from .model.bddthomas import get_membresData
from .model.bddthomas import del_membreData
from .model.bddthomas import get_themes
from .model.bddthomas import add_theme
from .model.bddthomas import delete_theme
from werkzeug.utils import secure_filename
import pandas, os
from .controller.function import messageInfo
from .model.bdd import exist 
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/files/'

def view2(app) :
    @app.route("/register", methods=['POST'])
    def register():
        if request.form['password'] != request.form['password2'] :
            session["infoRouge"] = "Les deux mots de passe doivent être identiques"
            params = messageInfo()
            return render_template("creation_compte.html.jinja", **params)
        identifiant = request.form['identifiant']
        if exist(identifiant):
            session["infoRouge"] = "Un compte avec cet identifiant existe déjà"
            params = messageInfo()
            return render_template("creation_compte.html.jinja", **params)
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
        if session.get("privilege") == "admin" :
            listeMembres = get_membresData()
            params ={
            'liste':listeMembres
            }
            #params = f.messageInfo(params)
            return render_template("sgbd.html.jinja", **params)
        else : 
            return redirect("/index")
    
    @app.route("/suppMembre/<user_id>")
    def suppMembre(user_id=""):
        del_membreData(user_id)
        if "errorDB" not in session:
            session["infoVert"]="L'utilisateur a bien été supprimé"
        else:
            session["infoRouge"] = "Problème suppression utilisateur"
        return redirect("/sgbd")

    @app.route('/gestion_reglementation', methods=['GET', 'POST'])
    def gestion_reglementation():
        if session.get("privilege") == "admin":
            message = session.pop('message', None)
            category = session.pop('category', None)
            search = None

            if request.method == 'POST':
                if 'delete' in request.form:
                    theme_id = request.form['theme_id']
                    delete_theme(theme_id)
                    session['message']  = "Le thème a bien été supprimé."
                    session['category'] = 'success'
                    return redirect(url_for('gestion_reglementation'))

                if 'add' in request.form:
                    nom         = request.form['nom'].strip()
                    eurvoc_name = request.form['eurvoc_name'].strip()
                    add_theme(nom, eurvoc_name)
                    session['message']  = "Le thème a bien été ajouté."
                    session['category'] = 'success'
                    return redirect(url_for('gestion_reglementation'))

                if 'search' in request.form:
                    search = request.form.get('search_term', '').strip()

            themes = get_themes(search)
            return render_template(
                'gestion_reglementation.html.jinja',
                themes=themes,
                message=message,
                category=category,
                search=search
            )
        else:
            return redirect(url_for('login'))
