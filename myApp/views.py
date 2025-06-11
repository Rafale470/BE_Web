from flask import Flask, render_template, session, redirect, url_for, request, flash, abort, jsonify
from .model.bdd import verifAuthData,get_eurvoc_uri_from_uid
from .controller.function import messageInfo
from myApp.model.cellar import get_eurovoc_themes, get_works_by_eurovoc_uri, get_details_work_by_eurovoc_uri, get_work_by_uri
import requests
from .viewsthomas import view2


app = Flask(__name__)   
view2(app)
app.template_folder = "template"
app.static_folder = "static"
app.config.from_object('myApp.config')

@app.route("/")
def index():
       params = messageInfo()
       return render_template("index.html.jinja", **params)

@app.route("/index")
def ind():
       return redirect(url_for("index"))

@app.route("/A_propos")
def propos():
       return render_template("A_propos.html.jinja")

@app.route('/login', methods=['POST']) 
def login():

       username = request.form['username']  
       password = request.form['password']  
       success, user = verifAuthData(username, password)
       print(f"{username},{password},{success}")
       if success :
              session["infoVert"]="Authentification réussie"
              session.update(user)
              session["logged"] = True
              return redirect(url_for('index'))
       else :
              session["infoRouge"] = "Erreur authentification"
              params = messageInfo()
              return render_template("login.html.jinja", **params)


@app.route("/login")
def loginfonction():
       return render_template("login.html.jinja")

@app.route("/register")
def ccfonction():
       return render_template("creation_compte.html.jinja")

@app.route("/logout")
def logoutfonction():
       session.clear()
       session["infoBleu"]="Déconnexion réussie"
       return redirect(url_for('index'))

@app.route('/ajax/eurovoc_suggest')
def eurovoc_suggest():
    q = request.args.get('q', '')
    results = get_eurovoc_themes(q)
    # Retourne une liste d'objets {uri, label}
    return jsonify([{'uri': uri, 'label': label} for uri, label in results.items()])

@app.route('/search_cellar', methods=['GET'])
def search_cellar():
    eurovoc_label = request.args.get('eurovoc', '')
    eurovoc_uri = request.args.get('eurovoc_uri', '')
    works = None

    # Suggestions pour le champ (optionnel, utile si tu veux pré-remplir)
    eurovoc_suggestions = get_eurovoc_themes(eurovoc_label) if eurovoc_label else {}

    # Si un thème a été choisi (URI présente), on cherche les textes associés
    if eurovoc_uri:
       print(f"Recherche des textes pour l'URI Eurovoc: {eurovoc_uri}")
       works = get_works_by_eurovoc_uri(eurovoc_uri)
       print(f"Nombre de textes trouvés: {len(works) if works else 0}")

    return render_template(
        'search.html.jinja',
        eurovoc_label=eurovoc_label,
        eurovoc_uri=eurovoc_uri,
        eurovoc_suggestions=eurovoc_suggestions,
        works=works
    )

@app.route('/recherche')
def recherche(): 
    user_id= session.get('user_id')
    eurovocs_uri = get_eurvoc_uri_from_uid(user_id)
    resultats = get_details_work_by_eurovoc_uri(eurovocs_uri)
    for resultat in resultats :
        eurovocs = get_work_by_uri(resultat['work_uri'])["eurovocs"]
        resultat['eurovocs'] = eurovocs
    return render_template("resultats.html.jinja", resultats=resultats)

@app.route('/document/<string:celex>')
def eurlex_document(celex):
    url = f"https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:{celex}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    except Exception as e:
        abort(500, f"Erreur lors du chargement de la page Eur-Lex : {e}")

    return render_template("document.html.jinja", content=html_content)
