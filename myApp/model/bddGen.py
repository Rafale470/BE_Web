import mysql.connector
from flask import session
from ..config import DB_SERVER, COLOR


###################################################################################
# connexion au serveur de la base de données

def connexion():
    try:
        cnx = mysql.connector.connect(**DB_SERVER)
        return cnx
    except mysql.connector.Error as err:
        session['errorDB'] = format(err)+" <br /> Veuillez vérifier les paramètres dans config.py"
        #affichage dans terminal
        print(COLOR['red'] + session['errorDB'] + COLOR['end'])  
        return None
    
    
#################################################################################
# Requête select avec fetchAll
def selectData(cnx, sql, param, msg):
   
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(sql, param)
        dict = cursor.fetchall() 
        cursor.close()
        #session['successDB'] = msg['success']
        print(COLOR['green'] +msg['success'] + COLOR['end']) #affichage dans terminal
    except mysql.connector.Error as err:
        dict = None
        session['errorDB'] = msg['error']+": {}".format(err)
        #affichage dans terminal
        print(COLOR['red'] + sql + COLOR['end'])
        print(COLOR['red'] + session['errorDB'] + COLOR['end'])  
    
    return dict

#################################################################################
# Requête select avec fetchOne
def selectOneData(cnx, sql, param, msg):
   
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(sql, param)
        dict = cursor.fetchone()  
        cursor.close()
        #session['successDB'] = msg['success']
        print(COLOR['green'] +msg['success'] + COLOR['end']) #affichage dans terminal
    except mysql.connector.Error as err:
        dict = None
        session['errorDB'] = msg['error']+": {}".format(err)
        #affichage dans terminal
        print(COLOR['red'] + sql + COLOR['end'])
        print(COLOR['red'] + session['errorDB'] + COLOR['end'])  
    
    return dict

#################################################################################
# Requête insert 
def addData(cnx, sql, param, msg):
      
    try:
        cursor = cnx.cursor()
        cursor.execute(sql, param)
        lastId = cursor.lastrowid  # récupère le dernier id généré par le serveur sql
        cnx.commit()
        cursor.close()
        #session['successDB'] = msg['success']
        print(COLOR['green'] +msg['success'] + COLOR['end']) #affichage dans terminal
    except mysql.connector.Error as err:
        lastId = None
        session['errorDB'] = msg['error']+": {}".format(err)
        #affichage dans terminal
        print(COLOR['red'] + sql + COLOR['end'])
        print(COLOR['red'] + session['errorDB'] + COLOR['end']) 
    return lastId

#################################################################################
# Requête insert avec plusieurs insertions
def addManyData(cnx, sql, param, msg):
    
    try:
        cursor = cnx.cursor()
        cursor.executemany(sql, param) #plusieurs insertions
        lastId = cursor.lastrowid  # récupère le dernier id généré par le serveur sql
        cnx.commit()
        cursor.close()
        #session['successDB'] = msg['success']
        print(COLOR['green'] +msg['success'] + COLOR['end']) #affichage dans terminal
    except mysql.connector.Error as err:
        lastId = None
        session['errorDB'] = msg['error']+": {}".format(err)
        #affichage dans terminal
        print(COLOR['red'] + sql + COLOR['end'])
        print(COLOR['red'] + session['errorDB'] + COLOR['end']) 
        
    return lastId

#################################################################################
# Requête delete
def deleteData(cnx, sql, param, msg):
    
    try:
        cursor = cnx.cursor()
        cursor.execute(sql, param)
        cnx.commit()
        cursor.close()
        #session['successDB'] = msg['success']
        print(COLOR['green'] +msg['success'] + COLOR['end']) #affichage dans terminal
       
    except mysql.connector.Error as err:
        session['errorDB'] = msg['error']+": {}".format(err)
        #affichage dans terminal
        print(COLOR['red'] + sql + COLOR['end'])
        print(COLOR['red'] + session['errorDB'] + COLOR['end'])

#################################################################################
# Requête update
updateData = deleteData