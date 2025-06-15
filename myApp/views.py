from flask import Flask, render_template, session, redirect, url_for, request, flash, abort, jsonify, Response
from .model.bdd import verifAuthData,get_eurvoc_uri_from_uid, add_favorite, del_favorite, get_favorite_by_user_and_celex, get_favoris_user
from .controller.function import messageInfo
from myApp.model.cellar import get_eurovoc_themes, get_works_by_eurovoc_uri, get_details_work_by_eurovoc_uri, get_work_by_uri
import requests
from .viewsthomas import view2
from bs4 import BeautifulSoup


app = Flask(__name__)   
view2(app)
app.template_folder = "template"
app.static_folder = "static"
app.config.from_object('myApp.config')

@app.route("/")
def index():
    params = messageInfo()
    page = request.args.get('page', 1, type=int)
    per_page = 5
    resultats = get_details_work_by_eurovoc_uri(["http://eurovoc.europa.eu/4408"], limit=(page+1)*per_page)
    resultats = [r for r in resultats if r is not None]
    for resultat in resultats :
        eurovocs = get_work_by_uri(resultat['work_uri'])["eurovocs"]
        resultat['eurovocs'] = eurovocs
    total = len(resultats)
    start = (page - 1) * per_page
    end = start + per_page
    resultats = resultats[start:end]
    return render_template("index.html.jinja",
                           resultats=resultats,
                           page=page,
                           total=total,
                           per_page=per_page,
                           **params)


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

@app.route('/feed')
def feed():
    params = messageInfo()
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    page = request.args.get('page', 1, type=int)
    per_page = 10
    eurovocs_uri = get_eurvoc_uri_from_uid(user_id)
    resultats = get_details_work_by_eurovoc_uri(eurovocs_uri, limit=(page+1)*per_page)
    for resultat in resultats :
        eurovocs = get_work_by_uri(resultat['work_uri'])["eurovocs"]
        resultat['eurovocs'] = eurovocs
        
        favori = get_favorite_by_user_and_celex(user_id, resultat['celex'])
        if favori:
            resultat['favori_existe'] = True
            resultat['nom_favori'] = favori[0]
        else:
            resultat['favori_existe'] = False

    total = len(resultats)
    start = (page - 1) * per_page
    end = start + per_page
    resultats = resultats[start:end]

    return render_template("feed.html.jinja",
                           resultats=resultats,
                           page=page,
                           total=total,
                           per_page=per_page,
                           **params)



@app.route('/eurlex_content/<string:celex>')
def eurlex_content(celex):
    url = f"https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:{celex}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # On parse le HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # On insère le CSS d'Eur-Lex
        link_tag = soup.new_tag("link", rel="stylesheet", href="https://eur-lex.europa.eu/content/css/eurlex.css")
        if soup.head:
            soup.head.insert(0, link_tag)
        else:
            soup.insert(0, link_tag)

        cleaned_html = str(soup)
        return Response(cleaned_html, mimetype='text/html')

    except Exception as e:
        abort(500, f"Erreur lors du chargement de la page Eur-Lex : {e}")
        
@app.route('/document/<string:celex>')
def eurlex_document(celex):
    return render_template("document.html.jinja", celex=celex)

@app.route('/ajouter_favori', methods=['POST'])
def ajouter_favori():
    celex = request.form.get('celex')
    nom_favori = request.form.get('nom_favori')

    if not celex or not nom_favori:
        session["infoRouge"]="Impossible d'ajouter le favori"
        return redirect(url_for('feed'))
    
    user_id = session.get('user_id')
    add_favorite(user_id, celex, nom_favori)
    print(user_id, celex, nom_favori)
    session["infoVert"]="Favori ajouté avec succès"
    return redirect(url_for('feed'))

@app.route('/supprimer_favori', methods=['POST'])
def supprimer_favori():
    celex = request.form.get('celex')
    user_id = session.get('user_id')

    if not celex or not user_id:
        session["infoRouge"] = "Impossible de supprimer le favori"
        return redirect(url_for('feed'))

    del_favorite(user_id, celex)

    session["infoVert"] = "Favori supprimé avec succès"
    return redirect(url_for('feed'))

@app.route('/mes_favoris')
def mes_favoris():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    favoris = get_favoris_user(user_id)

    params = messageInfo()  

    return render_template("mes_favoris.html.jinja", favoris=favoris, **params)

@app.route('/del_favori', methods=['POST'])
def del_favori():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    celex = request.form.get('celex')

    if not celex:
        session["infoRouge"] = "Impossible de supprimer ce favori."
        return redirect(url_for('mes_favoris'))

    del_favorite(user_id, celex)

    session["infoVert"] = "Favori supprimé avec succès."
    return redirect(url_for('mes_favoris'))