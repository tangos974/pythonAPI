from fastapi import FastAPI
from small_python_api.users import users_db
#J'ai préféré mettre la BDD dans un autre fichier users.py
#Je trouve ça légèrement plus réaliste

api = FastAPI(
    title='My API'
)

#Message de bienvenue
@api.get('/')
def get_index():
    return{'message': 'Bienvenue sur mon API'}

#Base de données en entier
@api.get('/users')
def get_all_users():
    return users_db

#Toutes les données d'un utilisateur ssi userid est fourni
#Sinon, ou si user id n'est pas dans BDD, renvoie dic vide
@api.get('/users/{userid:int}')
def get_user(userid: int):
    for user in users_db:
        if user['user_id'] == userid:
            return user
    return {} 

#Renvoie nom correspondant à l'userid
#Si userid pas utilisé, retourne dic vide
@api.get('/users/{userid:int}/name')
def get_username(userid: int):
    for user in users_db:
        if user['user_id'] == userid:
            return user['name']
    return {} 

#Autre option plus rapide, mais moins robuste
#car marche ssi la bdd (ici liste de dics python)
#est dans l'ordre:
"""
@api.get('/users/{userid:int}/name')
def get_username(userid: int):
    if 1 <= userid <= len(users_db):
        return users_db[userid - 1]['name']
    return {}
"""

#Renvoie souscription correspondant à l'userid
#Si userid pas utilisé, retourne dic vide
@api.get('/users/{userid:int}/subscription')
def get_user_subscritpion(userid: int):
    for user in users_db:
        if user['user_id'] == userid:
            return user['subscription']
    return {} 
