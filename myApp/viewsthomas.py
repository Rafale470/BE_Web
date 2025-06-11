from flask import Flask, g, render_template, session, redirect, url_for, request
import hashlib
import re
from .model.bddthomas import add_membreData
from .model.bddthomas import get_membresData
from .model.bddthomas import del_membreData
from .model.bddthomas import get_themes
from .model.bddthomas import add_theme
from .model.bddthomas import delete_theme
from werkzeug.utils import secure_filename
from .model.bddthomas import delete_user_theme
from .model.bddthomas import add_user_theme
from .model.bddthomas import get_user_theme_ids
from .model.bddthomas import get_user_by_id
from .model.bddthomas import update_user_info
from .model.bddthomas import change_user_password
from .model.bddthomas import get_prefs_by_user
from .model.bddthomas import get_all_themes
import pandas, os
from .controller.function import messageInfo
from .model.bdd import exist
from .model.bdd import mail_exist 
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
        email = request.form['mail']
        print(f"mail={email}")
        if mail_exist(email):
            session["infoRouge"] = "Un compte avec cet adresse mail existe déjà"
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

    @app.route("/sgbd", methods=['GET', 'POST'])   
    def sgbd():
        if session.get("privilege") != "admin":
            return redirect("/index")

        # ---------- Actions POST ----------
        if request.method == 'POST':
            user_id  = request.form['user_id']
            if 'delete_pref' in request.form:
                delete_user_theme(user_id, request.form['theme_id'])
                session["infoVert"]="Préférence supprimée"
            elif 'add_pref' in request.form:
                add_user_theme(user_id, request.form['theme_id'])
                session["infoVert"]="Préférence ajoutée"
            return redirect(url_for('sgbd'))

        # ---------- Données d’affichage ----------
        users       = get_membresData()
        prefs_by_id = get_prefs_by_user()
        all_themes  = get_all_themes()         # pour les menus “Ajouter”
        print(prefs_by_id)
        print(all_themes)
        

        return render_template("sgbd.html.jinja",
                            liste=users,
                            preferences_by_user=prefs_by_id,
                            all_themes=all_themes)
        
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
        if session.get("privilege") == "admin" :
            message  = session.pop('message', None)
            category = session.pop('category', None)
            search   = None

            if request.method == 'POST':
                if 'search' in request.form:
                    search = request.form.get('search_term', '').strip()

                elif 'delete' in request.form:
                    delete_theme(request.form['theme_id'])
                    session['message']  = "Le thème a bien été supprimé."
                    session['category'] = 'success'
                    return redirect(url_for('gestion_reglementation'))

                elif 'add' in request.form:
                    label = request.form['eurovoc'].strip()
                    uri   = request.form['eurovoc_uri'].strip()

                    m = re.search(r'(\d+)$', uri)
                    eurvoc_id = m.group(1) if m else uri

                    add_theme(label, eurvoc_id)
                    session['message']  = f"Thème « {label} » ajouté (ID {eurvoc_id})."
                    session['category'] = 'success'
                    return redirect(url_for('gestion_reglementation'))

            themes = get_themes(search)
            return render_template(
                'gestion_reglementation.html.jinja',
                themes=themes,
                message=message,
                category=category,
                search=search
            )
        else : 
            return redirect("/index")
            
    @app.route('/gestion_user_reglementation', methods=['GET', 'POST'])
    def gestion_user_reglementation():
        # ── sécurité : utilisateur connecté ───────────────────────────
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        # ── messages flash ────────────────────────────────────────────
        message  = session.pop('message', None)
        category = session.pop('category', None)
        search   = None

        # ── POST : filtrer / ajouter / retirer ────────────────────────
        if request.method == 'POST':
            if 'search' in request.form:
                search = request.form.get('search_term','').strip()

            elif 'user_add' in request.form:
                theme_id = request.form['theme_id']
                add_user_theme(user_id, theme_id)
                session['message']  = "Thème ajouté à vos préférences."
                session['category'] = 'success'
                return redirect(url_for('gestion_user_reglementation'))

            elif 'user_delete' in request.form:
                theme_id = request.form['theme_id']
                delete_user_theme(user_id, theme_id)
                session['message']  = "Thème retiré de vos préférences."
                session['category'] = 'success'
                return redirect(url_for('gestion_user_reglementation'))

        # ── données pour l’affichage ──────────────────────────────────
        themes           = get_themes(search)            # tous les thèmes (avec filtre)
        user_theme_ids   = set(get_user_theme_ids(user_id))

        return render_template(
            'gestion_user_reglementation.html.jinja',
            themes=themes,
            user_theme_ids=user_theme_ids,
            message=message,
            category=category,
            search=search
        )
        
    @app.route('/mon_compte', methods=['GET', 'POST'])
    def mon_compte():
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))

        message  = session.pop('message', None)
        category = session.pop('category', None)
        user     = get_user_by_id(user_id)

        # ───── POST : deux formulaires distincts ─────────────────────
        if request.method == 'POST':

            # 1) Infos générales
            if 'update_info' in request.form:
                update_user_info(
                    user_id,
                    request.form['username'].strip(),
                    request.form['nom'].strip(),
                    request.form['prenom'].strip(),
                    request.form['email'].strip()
                )
                session['message']  = "Profil mis à jour."
                session['category'] = 'danger'
                return redirect(url_for('mon_compte'))

            # 2) Mot de passe
            elif 'update_pass' in request.form:
                if request.form['new_password'] != request.form['confirm_password']:
                    session['message']  = "Les deux mots de passe ne correspondent pas."
                    session['category'] = 'danger'
                    return redirect(url_for('mon_compte'))

                # Vérifie l'ancien mot de passe
                old_hash = hashlib.sha256(
                    request.form['old_password'].encode()).hexdigest()
                if old_hash != user['password']:
                    session['message']  = "Mot de passe actuel incorrect."
                    session['category'] = 'danger'
                    return redirect(url_for('mon_compte'))

                # Hash du nouveau mot de passe
                new_hash = hashlib.sha256(
                    request.form['new_password'].encode()).hexdigest()
                change_user_password(user_id, new_hash)

                session['message']  = "Mot de passe changé."
                session['category'] = 'success'
                return redirect(url_for('mon_compte'))
            #######################################################
        # ── messages flash ────────────────────────────────────────────
        message  = session.pop('message', None)
        category = session.pop('category', None)
        search   = None

        # ── données pour l’affichage ──────────────────────────────────
        themes           = get_themes(search)            # tous les thèmes (avec filtre)
        user_theme_ids   = set(get_user_theme_ids(user_id))

        return render_template(
            'Ma_page.html.jinja',
            themes=themes,
            user_theme_ids=user_theme_ids,
            message=message,
            category=category,
            search=search
        )

        # ───── GET : affiche la page ─────────────────────────────────
        print(f"{user}")
        return render_template("Ma_page.html.jinja", user=user, message=message,category= category)
    
    
    #permet d'avoir user à dispo dans tous les templates
    @app.before_request
    def load_current_user():
        """Charge l’utilisateur courant à chaque requête s’il est connecté."""
        user_id = session.get("user_id")
        g.user = get_user_by_id(user_id) if user_id else None

    @app.context_processor
    def inject_user():
        """Injecte automatiquement 'user' dans tous les templates."""
        return {"user": g.user}