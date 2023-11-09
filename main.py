from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime
from users import users_db
#J'ai préféré mettre users_db dans un autre fichier users.py


class User(BaseModel):
    """Un utilisateur
    """
    userid: Optional[int] = None
    name: str
    subscription: str

class MyException(Exception):
    def __init__(self,
                 name : str,
                 date: str):
        self.name = name
        self.date = date


api = FastAPI(
    title='My API',
    description="My own API powered by FastAPI.",
    version="1.0",
)

responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}


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
    """
    Renvoie toutes les données d'un utilisateur ssi userid est fourni
    sinon, ou si user id n'est pas dans BDD, renvoie dictionnaire vide
    """
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return user
    except IndexError:
        return {}

@api.get('/users/{userid:int}/name')
def get_username(userid: int):
    """
    Renvoie nom correspondant à l'userid
    Si userid pas utilisé, retourne dic vide
    """
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'name': user['name']}
    except IndexError:
        return {}

@api.get('/users/{userid:int}/subscription')
def get_user_subscritpion(userid: int):
    """
    Renvoie souscription correspondant à l'userid
    Si userid pas utilisé, retourne dic vide
    """
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'subscription': user['subscription']}
    except:
        return{}
    
@api.post('/users')
def post_user(user: User):
    """
    POST le nouvel utilisateur, lui assignant automatiquement
    un nouvel userid
    """
    new_id = max(users_db, key=lambda u: u.get('user_id'))['user_id']
    new_user = {
        'user_id': new_id + 1,
        'name': user.name,
        'subscription': user.subscription
    }
    users_db.append(new_user)

    return new_user

@api.put('/users/{userid:int}')
def put_user(user: User, userid: int):
    """
    Change le nom et la souscription d'un utilisateur déjà existant
    """
    try:
        old_user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        users_db.remove(old_user)

        old_user['name'] = user.name
        old_user['subscription'] = user.subscription

        users_db.append(old_user)
        return old_user

    except IndexError:
        return{}

@api.delete('/users/{userid:int}')
def delete_user(user: User, userid: int):
    """
    Supprime un utilisateur
    """
    try:
        old_user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        users_db.remove(old_user)
        return {
            'userid': userid,
            'deleted': True
            }
    except IndexError:
        return{}