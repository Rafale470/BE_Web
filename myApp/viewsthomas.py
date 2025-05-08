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
        print("dans addmembre")
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
    
    @app.route("/suppMembre/<idUser>")
    def suppMembre(idUser=""):
        del_membreData(idUser)
        if "errorDB" not in session:
            session["infoVert"]="L'utilisateur a bien été supprimé"
        else:
            session["infoRouge"] = "Problème suppression utilisateur"
        return redirect("/sgbd")
    
    

    """
    @app.route("/gestion_users")
    def gestion_users():
        return render_template("gestion_users.html")
    
    @app.route("/gestion_users", methods=["GET", "POST"])
    def gestion_users():
        if request.method == "POST":
            # 1. Récupération du fichier
            if 'testFile' in request.files:
                file = request.files['testFile']
                filename = secure_filename(file.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)  # sauvegarde du fichier sur le serveur

                # 2. Lecture du fichier Excel en liste de dicts
                xls = pandas.read_excel(path)
                data = xls.to_dict('records')

                # 3. Sauvegarde en base de données
                #    adapter selon votre module bdd.saveDataFromFile()
                saveDataFromFile(data)
                if "errorDB" not in session:
                    session["infoVert"] = "Données importées avec succès"
                else:
                    session["infoRouge"] = "Erreur lors de l’enregistrement"
            return redirect("/gestion_users")
         # Méthode GET : récupération de tous les utilisateurs
        liste = gmd()
        params = {"liste": liste}
    
        return render_template("gestion_users.html", **params)
    
    @app.route("/suppMembre/<idUser>")
    def suppMembre(idUser):
        del_membreData(idUser)
        if "errorDB" not in session:
            session["infoVert"] = "Utilisateur supprimé"
        else:
            session["infoRouge"] = "Erreur suppression"
        return redirect("/gestion_users")


    @app.route("/updateStatut", methods=["POST"])
    def updateStatut():
        idUser   = request.form['pk']
        newValue = request.form['value']
        update_membreData("statut", idUser, newValue)
        return "1"
    """
    # @app.route("/gestion_users", methods=['POST'])
    # def fichiersUpload():
    #     if "testFile" in request.files:
    #         file = request.files['testFile']
    #     filename = secure_filename(file.filename)
    #     print(os.path.join(UPLOAD_FOLDER, filename))
    #     file.save(os.path.join(UPLOAD_FOLDER, filename))
    #     xls = pandas.read_excel(UPLOAD_FOLDER+file.filename)
    #     data = xls.to_dict('records')
    #     print([file.filename, data])
    #     bddGen.saveDataFromFile(data)
    #     if "errorDB" not in session:
    #         session["infoVert"] = "Données sauvegardées en BDD"
    #         return redirect("/gestion_users")
    #     else: # problème enregistrement
    #         session["infoRouge"]="Problème enregistrement des données"
    #         return redirect("/gestion_users")
        
    # @app.route("/exportToExcel")
    # def exportToExcel():
    #     listeMembre = bddGen.get_membresData()
    # wb = Workbook()
    # sheet = wb.active
    # headers = [x for x in listeMembre[0]]
    # for index, value in enumerate(headers):
    #     sheet.cell(row=1, column=index+1).value = value
    # for i, x in enumerate(listeMembre):
    #     for idx, value in enumerate(x.values()):
    #         sheet.cell(row=i+2, column=idx+1).value = value
    # nomFile = 'export.xls'
    # wb.save(UPLOAD_FOLDER+nomFile)
    # return redirect(UPLOAD_FOLDER+nomFile)