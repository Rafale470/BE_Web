import mysql.connector
from flask import session
from myApp.config import DB_SERVER, COLOR
import hashlib
from . import bddGen

def get_eurvoc_uri_from_uid(user_id):
    cnx = bddGen.connexion()
    if cnx is None:
        return None
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT eurvoc_name FROM Themes JOIN Preferences ON Themes.theme_id = Preferences.theme_id JOIN Users ON Preferences.user_id = Users.user_id WHERE Users.user_id = %s"
    cursor.execute(sql, [user_id])
    res = cursor.fetchall()
    cursor.close()
    cnx.close()

    # On renvoie les uris des thèmes s'il y en a
    if len(res) > 0:
        return ["http://eurovoc.europa.eu/" + str(row['eurvoc_name']) for row in res]
    else:
        return []
 

def verifAuthData(login, password):
    cnx = bddGen.connexion()
    password = hashlib.sha256(password.encode())
    passwordC = password.hexdigest()
    if cnx is None:
        return None
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT user_id, username, nom, prenom, email, privilege FROM Users WHERE username = %s AND password = %s LIMIT 1"
    cursor.execute(sql, [login, passwordC])
    res = cursor.fetchall()
    cursor.close()
    cnx.close()
    # On vérifie si on a trouvé un utilisateur
    # On renvoie un booléen et l'utilisateur s'il existe
    success = (len(res) == 1)
    return (success, res[0] if success else None)

def exist(login):
    cnx = bddGen.connexion()
    if cnx is None:
        return None
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT username FROM Users WHERE username = %s"
    cursor.execute(sql, [login])
    res = cursor.fetchall()
    cursor.close()
    cnx.close()
    success = (len(res) == 1)
    return (success)

def mail_exist(mail):
    cnx = bddGen.connexion()
    if cnx is None:
        return None
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT email FROM Users WHERE email = %s"
    cursor.execute(sql, [mail])
    res = cursor.fetchall()
    cursor.close()
    cnx.close()
    success = (len(res) == 1)
    return (success)