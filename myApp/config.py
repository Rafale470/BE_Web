ENV = "development"
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0 #vider le cache
SECRET_KEY="maCleSuperSecurisee"

COLOR ={
'header' : '\033[95m',
'blue' : '\033[94m',
'green' : '\033[92m',
'orange' : '\033[93m',
'red' : '\033[31m',
'end' : '\033[0m',
}

#Configuration du serveur web

WEB_SERVER = {
    "host": "10.3.110.2",
    "port":8081,
}

#Configuration du serveur de BDD

DB_SERVER = {
    "user": "root",
    "password": "mysql",
    "host": "localhost",
    "port": 3306, #8889 si MAC
    "database": "IENAC24_Alerte_reglementation_aeronautique", #nom de la BDD
    "raise_on_warnings": True
}   