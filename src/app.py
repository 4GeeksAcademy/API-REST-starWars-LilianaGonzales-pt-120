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
from models import db, User, Character, Vehicle, Planet, user_character, user_planet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# @app.route('/users', methods=["POST"])
# def create_user():
#     data = request.get_json()
#     user = User(
#         username= data.get('username'),
#         email = data.get('email'),
#         password = data.get('password'),
#         subscription = data.get('subscription')# va si el tipo de dato el solo DateTime
#     )
#     db.session.add(user)
#     db.session.commit()

#     print(data)
#     return "ok", 200

@app.route('/users', methods=["GET"])
def get_users():
    users = list(db.session.execute(db.select(User)).scalars())
    print(users)
    result = [user.to_dict() for user in users]
    print(result)
    return jsonify(result)


@app.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    user = db.session.get(User, id)
    print(user.to_dict())
    return jsonify(user.to_dict_all_data()), 200


@app.route('/users', methods=["POST"])
def create_user():
    data = request.get_json()
    user = User.create(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'))
    print(user)
    return jsonify(user.to_dict())


# character

@app.route('/characters', methods=["GET"])
def get_characters():
    characters = list(db.session.execute(db.select(Character)).scalars())
    print(characters)
    result = [character.to_dict() for character in characters]
    print(result)
    return jsonify(result)


@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = db.session.get(Character, id)
    print(character.list_vehicle)
    # return jsonify(character.to_dict()), 200
    return jsonify(character.to_dict_all_data()), 200


@app.route('/characters', methods=["POST"])
def create_character():
    data = request.get_json()
    character = Character.create(
        name=data.get('name'),
        gender=data.get('gender'),
        height=data.get('height'))
    print(character)
    return jsonify(character.to_dict())

# planets

@app.route('/planets', methods=["GET"])
def get_planets():
    planets = list(db.session.execute(db.select(Planet)).scalars())
    print(planets)
    result = [planet.to_dict() for planet in planets]
    print(result)
    return jsonify(result)


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = db.session.get(Planet, id)
    return jsonify(planet.to_dict()), 200


@app.route('/planets', methods=["POST"])
def create_planet():
    data = request.get_json()
    planet = Planet.create(
        name=data.get('name'),
        climate=data.get('climate'),
        population=data.get('population'))
    print(planet)
    return jsonify(planet.to_dict())

# vehicles


@app.route('/vehicles', methods=["POST"])
def create_vehicle():
    data = request.get_json()
    vehicle = Vehicle(
        name=data.get('name'),
        model=data.get('model'),
        passengers=data.get('passengers'),
        character_id=data.get('character_id')
    )
    db.session.add(vehicle)
    db.session.commit()
    print(vehicle)
    return 'ok', 200

 # user_character


@app.route('/users_characters', methods=["POST"])
def add_user_character():
    data = request.get_json()
    print(data)
    userCharacter = user_character.insert().values(
        # userCharacter = user_character(
        user_id=data.get('user_id'),
        character_id=data.get('character_id'),
        favorite=data.get('favorite')
    )
    db.session.execute(userCharacter)
    db.session.commit()
    print(userCharacter)
    return 'ok', 200

@app.route('/users_planets', methods=["POST"])
def add_user_planet():
    data = request.get_json()
    print(data)
    userPlanet = user_planet.insert().values(
        user_id=data.get('user_id'),
        planet_id=data.get('planet_id'),
        favorite=data.get('favorite')
    )
    db.session.execute(userPlanet)
    db.session.commit()
    print(userPlanet)
    return 'ok', 200

# @app.route('/characters/favorite/<int:user_id>', methods=["GET"])
# def get_user_character(user_id):
    # query = user_character.select().where(
    #     user_character.c.user_id == user_id,

    #    user_character.c.favorite == True
    # )
    # result = db.session.execute(query).mappings().all()
    # print(type.result)
    # return jsonify(result)







# def add_character_to_user(user_id, character_id):
#     favorite = request.json.get("favorite", False)

#     insert_stmt = user_character.insert().values(
#         user_id=user_id,
#         character_id=character_id,
#         favorite=favorite
#     )
#     db.session.execute(insert_stmt)
#     db.session.commit()

#     return jsonify({"msg": "Character added to user"}), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
