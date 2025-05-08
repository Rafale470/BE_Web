from flask import Flask, render_template, session, redirect, url_for, request, flash, abort
from .model.bdd import verifAuthData
from .controller.function import messageInfo


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
       user = {"user_id" : 1, "username" : "test", "password" : "532eaabd9574880dbf76b9b8cc00832c20a6ec113d682299550d7a6e0f345e25", "nom":"aaa","prenom":"bbb","email":"aaa@gmaol.com","privilege":"user"}

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

@app.route("/Ma_page")
def Ma_page():
       if session.get("logged") :
              params = messageInfo()
              return render_template("Ma_page.html.jinja", **params)
       else :
              params = messageInfo()
              return redirect(url_for("login"))

@app.route("/logout")
def logoutfonction():
       session.clear()
       return redirect(url_for("index"))

