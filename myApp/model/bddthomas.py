
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


def get_user_theme_ids(user_id):
    """Liste des theme_id déjà choisis par l’utilisateur."""
    cnx = bddGen.connexion()
    if cnx is None:
        return []
    cur = cnx.cursor()
    cur.execute("SELECT theme_id FROM Preferences WHERE user_id = %s;", (user_id,))
    ids = [row[0] for row in cur.fetchall()]
    cur.close(); cnx.close()
    return ids


def add_user_theme(user_id, theme_id):
    """Ajoute (user_id, theme_id) à user_themes si absent."""
    cnx = bddGen.connexion()
    if cnx is None:
        return
    sql = "INSERT IGNORE INTO Preferences (user_id, theme_id) VALUES (%s, %s);"
    bddGen.addData(cnx, sql, (user_id, theme_id),
                      {"success": "addUserThemeOK",
                       "error":   "Failed add user theme"})
    cnx.close()


def delete_user_theme(user_id, theme_id):
    """Retire la préférence utilisateur pour ce thème."""
    cnx = bddGen.connexion()
    if cnx is None:
        return
    sql = "DELETE FROM Preferences WHERE user_id=%s AND theme_id=%s;"
    bddGen.deleteData(cnx, sql, (user_id, theme_id),
                      {"success": "delUserThemeOK",
                       "error":   "Failed del user theme"})
    cnx.close()

def get_user_by_id(user_id):
    cnx = bddGen.connexion()
    c   = cnx.cursor(dictionary=True)
    c.execute("SELECT * FROM Users WHERE user_id=%s;", (user_id,))
    user = c.fetchone()
    c.close(); cnx.close()
    return user


def update_user_info(user_id, username, nom, prenom, email):
    cnx = bddGen.connexion()
    sql = """
      UPDATE Users
      SET username=%s, nom=%s, prenom=%s, email=%s
      WHERE user_id=%s;
    """
    bddGen.addData(cnx, sql,
                      (username, nom, prenom, email, user_id),
                      {"success": "updUserOK",
                       "error":   "Failed update user"})
    cnx.close()


def change_user_password(user_id, new_hash):
    cnx = bddGen.connexion()
    sql = "UPDATE Users SET password=%s WHERE user_id=%s;"
    bddGen.addData(cnx, sql,
                      (new_hash, user_id),
                      {"success": "updPassOK",
                       "error":   "Failed update pass"})
    cnx.close()
    
def get_prefs_by_user():
    """
    Renvoie un dictionnaire : { user_id: [ {theme_id, nom}, … ] }
    Un seul appel SQL pour éviter la boucle N+1.
    """
    cnx = bddGen.connexion()
    if cnx is None:
        return {}

    cur = cnx.cursor(dictionary=True)
    cur.execute("""
        SELECT p.user_id, t.theme_id, t.nom
        FROM Preferences AS p
        JOIN Themes      AS t ON t.theme_id = p.theme_id
        ORDER BY t.nom;
    """)
    prefs = {}
    for row in cur.fetchall():
        prefs.setdefault(row["user_id"], []).append(
            {"theme_id": row["theme_id"], "nom": row["nom"]}
        )
    cur.close(); cnx.close()
    return prefs

def get_all_themes():
    """Renvoie la liste complète des thèmes (id + nom)."""
    cnx = bddGen.connexion()
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT theme_id, nom FROM Themes ORDER BY nom;")
    rows = cur.fetchall()
    cur.close(); cnx.close()
    return rows

def get_favoris_by_user():
    """
    Renvoie { user_id: [ {cellar_id, nom}, … ] } pour remplir la colonne Favoris.
    """
    cnx = bddGen.connexion()
    if cnx is None:
        return {}

    cur = cnx.cursor(dictionary=True)
    cur.execute("""
        SELECT user_id, cellar_id, nom
        FROM Favoris
        ORDER BY nom;
    """)
    favs = {}
    for row in cur.fetchall():
        favs.setdefault(row["user_id"], []).append(
            {"cellar_id": row["cellar_id"], "nom": row["nom"]}
        )
    cur.close(); cnx.close()
    return favs


def delete_user_favori(user_id, cellar_id):
    cnx = bddGen.connexion()
    if cnx is None:
        return
    sql = "DELETE FROM Favoris WHERE user_id=%s AND cellar_id=%s;"
    bddGen.deleteData(cnx, sql, (user_id, cellar_id),
                      {"success": "delFavOK",
                       "error":   "Failed delete favori"})
    cnx.close()