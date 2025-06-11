from flask import Flask, render_template, session, redirect, url_for, request, flash, abort, jsonify
from .model.bdd import verifAuthData
from .controller.function import messageInfo
from myApp.model.cellar import get_eurovoc_themes, get_works_by_eurovoc_uri

from .viewsthomas import view2
from .model.bddthomas import get_user_by_id


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
    
    
    
resultats = [
    {
        "titre": "Directive 2010/75/UE relative aux émissions industrielles",
        "lien_eli": "http://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32010L0075",
        "numero_celex": "32010L0075",
        "forme": "Directive",
        "descripteur_eurovoc": "Pollution industrielle",
        "code_repertoire": "15.20.10.00",
        "base_juridique": "TFUE article 192",
        "date_document": "2010-11-24",
        "en_vigueur": "Oui",
        "date_prise_effet": "2010-12-01",
        "date_fin_validite": None
    },
    {
        "titre": "Règlement (UE) 2016/679 du Parlement européen et du Conseil",
        "lien_eli": "http://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679",
        "numero_celex": "32016R0679",
        "forme": "Règlement",
        "descripteur_eurovoc": "Protection des données",
        "code_repertoire": "20.15.30.00",
        "base_juridique": "TFUE article 16",
        "date_document": "2016-04-27",
        "en_vigueur": "Oui",
        "date_prise_effet": "2016-05-24",
        "date_fin_validite": None
    },
    {
        "titre": "Directive 2009/147/CE concernant la conservation des oiseaux sauvages",
        "lien_eli": "http://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32009L0147",
        "numero_celex": "32009L0147",
        "forme": "Directive",
        "descripteur_eurovoc": "Protection des oiseaux",
        "code_repertoire": "15.10.20.00",
        "base_juridique": "TFUE article 192",
        "date_document": "2009-11-30",
        "en_vigueur": "Oui",
        "date_prise_effet": "2010-01-15",
        "date_fin_validite": None
    },
    {
        "titre": "Règlement (UE) 2021/241 établissant la facilité pour la reprise et la résilience",
        "lien_eli": "http://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32021R0241",
        "numero_celex": "32021R0241",
        "forme": "Règlement",
        "descripteur_eurovoc": "Plan de relance",
        "code_repertoire": "03.60.20.00",
        "base_juridique": "TFUE articles 175 et 322",
        "date_document": "2021-02-12",
        "en_vigueur": "Oui",
        "date_prise_effet": "2021-02-19",
        "date_fin_validite": None
    },
    {
        "titre": "Directive (UE) 2018/2001 relative à la promotion de l'utilisation de l'énergie produite à partir de sources renouvelables",
        "lien_eli": "http://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32018L2001",
        "numero_celex": "32018L2001",
        "forme": "Directive",
        "descripteur_eurovoc": "Énergies renouvelables",
        "code_repertoire": "12.30.20.00",
        "base_juridique": "TFUE article 194",
        "date_document": "2018-12-11",
        "en_vigueur": "Oui",
        "date_prise_effet": "2018-12-24",
        "date_fin_validite": None
    }
]

@app.route('/recherche')
def recherche():
    # Ici tu appelles ta vraie fonction de recherche
    return render_template("resultats.html.jinja", resultats=resultats)

@app.route('/document/<numero_celex>')
def document(numero_celex):
    document = next((doc for doc in resultats if doc['numero_celex'] == numero_celex), None)
    if document is None:
        return "Document non trouvé", 404
    return render_template('document.html.jinja', document=document)
