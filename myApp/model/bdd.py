import mysql.connector
from flask import session
from myApp.config import DB_SERVER, COLOR
import hashlib
from . import bddGen

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