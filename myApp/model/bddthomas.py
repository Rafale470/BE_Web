
import mysql.connector
from flask import session
from myApp.config import DB_SERVER, COLOR
import hashlib
from . import bddGen


def add_membreData(identifiant, motpasse , nom , prenom, mail):
    cnx = bddGen.connexion()
    if cnx is None: 
        return None
    sql = "INSERT INTO Users (username, password, nom, prenom, email) VALUES (%s, %s, %s, %s, %s);"
    print("inséré")
    param = (identifiant, motpasse , nom , prenom, mail)
    msg = {
    "success":"addMembreOK",
    "error" : "Failed add membres data"
    }
    lastId = bddGen.addData(cnx, sql, param, msg)
    cnx.close()
    #dernier id créé = id du nouvel utilisateur
    return lastId

def get_membresData():
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = " SELECT * FROM Users"
    param = None
    msg = {
        "success":"OKmembres",
        "error" : "Failed get membres data"
    }
    listeMembre = bddGen.selectData(cnx, sql, param, msg)
    cnx.close()
    return listeMembre

def del_membreData(idUser):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "DELETE FROM Users WHERE user_id=%s;"
    param = (idUser,)
    msg = {
    "success":"suppMembreOK",
    "error" : "Failed del membres data"
    }
    bddGen.deleteData(cnx, sql, param, msg)
    cnx.close()




"""
def get_membresData():
    cnx = bddGen.connexion()
    if cnx is None:
        return None

    sql = "SELECT * FROM identification"
    msg = {
        "success": "OK get_membresData",
        "error":   "Failed get membres data"
    }
    listeMembres = bddGen.selectData(cnx, sql, None, msg)
    cnx.close()
    return listeMembres

def del_membreData(idUser):
    cnx = bddGen.connexion()
    if cnx is None:
        return None

    sql = "DELETE FROM identification WHERE idUser=%s;"
    param = (idUser,)
    msg = {
        "success": "suppMembreOK",
        "error":   "Failed del membres data"
    }
    bddGen.deleteData(cnx, sql, param, msg)
    cnx.close()

def update_membreData(champ, idUser, newValue):
    cnx = bddGen.connexion()
    if cnx is None:
        return None

    sql = f"UPDATE identification SET {champ}=%s WHERE idUser=%s;"
    param = (newValue, idUser)
    msg = {
        "success": "updateMembreOK",
        "error":   "Failed update membres data"
    }
    bddGen.updateData(cnx, sql, param, msg)
    cnx.close()

def saveDataFromFile(data):
    #Tronque puis insère en bloc.
    # 1) Truncate
    cnx = bddGen.connexion()
    if cnx is None:
        session['errorDB'] = "Impossible de se connecter à la BDD."
        return None
    bddGen.deleteData(cnx, "TRUNCATE TABLE identification;", None,
            {"success":"OK","error":"Échec truncate"})
    # 2) Prépare et exécute l'insert batch
    sql = ("INSERT INTO identification "
        "(username, password, nom, prenom, email) "
        "VALUES (%s, %s, %s, %s, %s);")
    params = [
        (d['username'], d['password'], d['nom'],
        d['prenom'], d['email'])
        for d in data
    ]
    last_id = bddGen.addManyData(cnx, sql, params,
                    {"success":"OK insert","error":"Échec insert"})
    cnx.close()
    return last_id"""