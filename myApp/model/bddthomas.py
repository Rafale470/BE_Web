
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