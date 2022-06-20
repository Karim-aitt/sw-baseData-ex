"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, People, Planets, User, Favorites, PeopleFavorites, PlanetsFavorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ----------------------------------------------------PEOPLE
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    all_people = list(map(lambda people: people.serialize(), people))
    return jsonify(all_people), 201

@app.route('/people', methods=['POST'])
def post_people():
    body = request.get_json()
    print(body)
    people = People(uid=body["uid"], name=body["name"])
    db.session.add(people)
    db.session.commit()
    return jsonify(people.serialize()), 201

@app.route('/people/<int:people_uid>', methods=['GET', 'PUT', 'DELETE'])
def people_single(people_uid):
    if request.method == 'GET':
        people = People.query.get(people_uid)
        if people is None:
            raise APIException("Persona no encontrada", 404)

        return jsonify(people.serialize())
    
    if request.method == 'PUT':
        print(people_uid)
        people = People.query.get(people_uid)
        print(people)
        # return "hi"
        if people is None:
           raise APIException("Persona no encontrada", 404)
        body = request.get_json()

        if not ("uid" in body):
            raise APIException("uid no encontrado", 404)

        people.uid = body["uid"]
        people.name = body["name"]
        db.session.commit()

        return jsonify(people.serialize())
    
    if request.method == 'DELETE':
        people = People.query.get(people_uid)
        if people is None:
            raise APIException("Person not found", 404)
        db.session.delete(people)
        db.session.commit()

        return jsonify(people.serialize())

# ----------------------------------------------------PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda planets: planets.serialize(), planets))
    return jsonify(all_planets), 201

@app.route('/planets', methods=['POST'])
def post_planets():
    body = request.get_json()
    print(body)
    planets = Planets(uid=body["uid"], name=body["name"])
    db.session.add(planets)
    db.session.commit()
    return jsonify(planets.serialize()), 201

@app.route('/planets/<int:planets_id>', methods=['GET', 'PUT', 'DELETE'])
def planets_single(planets_id):
    if request.method == 'GET':
        planets = Planets.query.get(planets_id)
        if planets is None:
            raise APIException("Planeta no encontrado", 404)

        return jsonify(planets.serialize())
    
    if request.method == 'PUT':
        planets = Planets.query.get(planets_id)
        if planets is None:
           raise APIException("Planeta no encontrado", 404)
        body = request.get_json()

        if not ("uid" in body):
            raise APIException("Parametro no encontrado", 404)

        planets.uid = body["uid"]
        planets.name = body["name"]
        db.session.commit()

        return jsonify(planets.serialize())
    
    if request.method == 'DELETE':
        planets = Planets.query.get(planets_id)
        if planets is None:
            raise APIException("Planet not found", 404)
        db.session.delete(planets)
        db.session.commit()
        
        return jsonify(planets.serialize())

# ----------------------------------------------------USERS
@app.route('/users', methods=['GET'])
def get_users():
    user = User.query.all()
    all_users = list(map(lambda user: user.serialize(), user))
    return jsonify(all_users), 201

@app.route('/user', methods=['POST'])
def post_user():
    body = request.get_json()
    print(body)
    user = User(name=body["name"], email=body["email"], password=body["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

# ----------------------------------------------------FAVORITES

# @app.route('/user/<int:user_id>/favorites', methods=['GET'])
# def get_user_favorites(user_id):
#     fav = Favorite.query.filter_by(user_id=user_id)
#     userFavorites = list(map(lambda fav: fav.serialize(), fav))
#     return jsonify(userFavorites), 201

# @app.route('/user/<int:user_id>/favorite/planets/<int:planets_id>', methods=['POST'])
# def post_user_planets_favorite(user_id, planets_id):
#     # body = request.get_json()
#     # print(body)
#     favorites = Favorite(user_id=user_id, planets_id=planets_id)
#     db.session.add(favorites)
#     db.session.commit()
#     return jsonify(favorites.serialize()), 201

# @app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
# def post_user_people_favorite(user_id, people_id):
#     # body = request.get_json()
#     # print(body)
#     favorites = Favorite(user_id=user_id, people_id=people_id)
#     db.session.add(favorites)
#     db.session.commit()
#     return jsonify(favorites.serialize()), 201

# ----------------------------------------------------FAVORITOS 2

@app.route('/user/<int:user_id>/favorites/people', methods=['GET'])
def get_people_fav(user_id):
    people_fav = PeopleFavorites.query.filter_by(user_id=user_id)
    if user_id is None:
        return "No hay personajes favoritos"

    userFavorites = list(map(lambda people_fav: people_fav.serialize(), people_fav))
    return jsonify(userFavorites),201

@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def pe_fav(user_id, people_id):
    favorites = PeopleFavorites(user_id=user_id, people_id=people_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(favorites.serialize()), 201

@app.route('/user/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_people_fav(user_id, people_id):
    deleteFav = PeopleFavorites.query.filter_by(user_id=user_id, people_id=people_id).one() #one devuelve el objeto encontrado, sin el one, devuelve el queryobject
    db.session.delete(deleteFav)
    db.session.commit()

    return jsonify(deleteFav.serialize()), 202

#------------------------------------------------------------------PLANETS

@app.route('/user/<int:user_id>/favorites/planets', methods=['GET'])
def get_planets_fav(user_id):
    planets_fav = PlanetsFavorites.query.filter_by(user_id=user_id)
    if user_id is None:
        return "No hay personajes favoritos"

    userFavorites = list(map(lambda planets_fav: planets_fav.serialize(), planets_fav))
    return jsonify(userFavorites),201

@app.route('/user/<int:user_id>/favorites/planets/<int:planets_id>', methods=['POST'])
def post_planets_fav(user_id, planets_id):
    favorites = PlanetsFavorites(user_id=user_id, planets_id=planets_id)
    db.session.add(favorites)
    db.session.commit()
    return jsonify(favorites.serialize()), 201

@app.route('/user/<int:user_id>/favorites/planets/<int:planets_id>', methods=['DELETE'])
def delete_planets_fav(user_id, planets_id):
    deleteFav = PlanetsFavorites.query.filter_by(user_id=user_id, planets_id=planets_id).one() #one devuelve el objeto encontrado, sin el one, devuelve el queryobject
    db.session.delete(deleteFav)
    db.session.commit()

    return jsonify(deleteFav.serialize()), 202

#------------------------------------------------------------------GET ALL USER FAVS
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_user_favorites(user_id):
    people = PeopleFavorites.query.filter_by(user_id=user_id)
    planets = PlanetsFavorites.query.filter_by(user_id=user_id)
    all_people_favorites = list(map(lambda people: people.serialize(), people))
    all_planets_favorites = list(map(lambda planets: planets.serialize(), planets))
    return jsonify(all_people_favorites, all_planets_favorites)
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
