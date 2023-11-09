from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from users import users_db
#J'ai préféré mettre users_db dans un autre fichier users.py


class User(BaseModel):
    userid: Optional[int] = None
    name: str
    subscription: str


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
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return user
    except IndexError:
        return {}

#Renvoie nom correspondant à l'userid
#Si userid pas utilisé, retourne dic vide
@api.get('/users/{userid:int}/name')
def get_username(userid: int):
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'name': user['name']}
    except IndexError:
        return {}

#Renvoie souscription correspondant à l'userid
#Si userid pas utilisé, retourne dic vide
@api.get('/users/{userid:int}/subscription')
def get_user_subscritpion(userid: int):
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'subscription': user['subscription']}
    except:
        return{}
    

#POST le nouvel utilisateur, ne prend pas d'argument ID
#car celui-ci est assigné automatiquement
@api.post('/users')
def post_user(user: User):
    new_id = max(users_db, key=lambda u: u.get('user_id'))['user_id']
    new_user = {
        'user_id': new_id + 1,
        'name': user.name,
        'subscription': user.subscription
    }
    users_db.append(new_user)

    return new_user

#PUT d'un utilisateur déjà existant, on met à jour son
#nom et sa souscription
@api.put('/users/{userid:int}')
def put_user(user: User, userid: int):
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
    try:
        old_user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        users_db.remove(old_user)
        return {
            'userid': userid,
            'deleted': True
            }
    except IndexError:
        return{}