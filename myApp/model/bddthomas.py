
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

def get_themes(search=None):
    cnx = bddGen.connexion()
    if cnx is None:
        return []
    cursor = cnx.cursor(dictionary=True)
    if search:
        sql = """
            SELECT theme_id, nom, eurvoc_name
            FROM Themes
            WHERE nom LIKE %s OR eurvoc_name LIKE %s
        """
        like = f"%{search}%"
        cursor.execute(sql, (like, like))
    else:
        sql = "SELECT theme_id, nom, eurvoc_name FROM Themes;"
        cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results

def add_theme(nom, eurvoc_name):
    cnx = bddGen.connexion()
    if cnx is None:
        return None
    sql = """
        INSERT INTO Themes (nom, eurvoc_name)
        VALUES (%s, %s);
    """
    params = (nom, eurvoc_name)
    msg = {
        "success": "addThemeOK",
        "error":   "Failed to add theme"
    }
    bddGen.addData(cnx, sql, params, msg)
    cnx.close()

def delete_theme(theme_id):
    cnx = bddGen.connexion()
    if cnx is None:
        return None
    sql = "DELETE FROM Themes WHERE theme_id = %s;"
    params = (theme_id,)
    msg = {
        "success": "delThemeOK",
        "error":   "Failed to delete theme"
    }
    bddGen.deleteData(cnx, sql, params, msg)
    cnx.close()