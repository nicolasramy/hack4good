# -*- coding: utf-8 -*-
import sys

# Flask
from flask import Flask, request, jsonify, make_response, abort

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from model import commute4good

# Flask Application
api = Flask(__name__)


@api.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


engine = create_engine("postgresql://%s:%s@%s:%s/%s" % (config.postgres.username,
                                                        config.postgres.password,
                                                        config.postgres.hostname,
                                                        config.postgres.port,
                                                        config.postgres.database
                                                        )
                       )

# Start session
Session = sessionmaker(bind=engine)
pg_session = Session()


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@api.route('/geoposition', methods=['POST'])
def new_position():
    if not request.json or not 'user_id' in request.json \
    or not 'lon' in request.json or not 'lat' in request.json:
        abort(400)

    geolocation = {
        "user_id": request.json['user_id'],
        "lon": request.json['lon'],
        "lat": request.json['lat']
    }

    # Save

    return jsonify(geolocation), 201


@api.route('/users/<int:user_id>', methods=['GET'])
def user_profil(user_id):

    users = pg_session.query(commute4good.User).filter_by(id=user_id)

    data = {
        "id": users[0].id,
        "firstname": users[0].firstname,
        "lastname": users[0].lastname,
        "pseudo": users[0].pseudo,
        "email": users[0].email,
        "photo_path": users[0].photo_path,
        "created_at": users[0].created_at,
        "last_accessed_at": users[0].last_accessed_at,
        "lon": users[0].lon,
        "lat": users[0].lat,
        "connected": users[0].connected
    }

    return jsonify(data)

#
## /users
#class Users(Resource):
#    def get(self, user_id):
#        #return {user_id: users[user_id]}
#        return {user_id: 'profil'}
#
#    def post(self, user_id):
#        if user_id is not None:
#            return {user_id: "404"}
#        else:
#            return {user_id: "Welcome X"}
#
#    def put(self, user_id):
#        return {user_id: "updated"}
#
#    def delete(self, user_id):
#        return {user_id: "disabled function for instance"}
#
#api.add_resource(Users, '/users/<int:user_id>')
#
#
## /users/login
#class UsersLogin(Resource):
#    # Authentificate users
#    def get(self):
#        return {"Authentification failed"}
#
#api.add_resource(UsersLogin, '/users/<int:user_id>')
#
#
## /users/nearest
#class UsersNearest(Resource):
#    # Find users
#    def get(self):
#        return {"No one found there."}
#
#api.add_resource(UsersNearest, '/users/nearest/<int:user_id>')
#
#
## /tags
#class Tags(Resource):
#    # Add tags
#    def post(self):
#        return {"May, the 4th be with you"}
#
#api.add_resource(Tags, '/tags/')
#
#
## /geoposition
#class Geoposition(Resource):
#    # Update position
#    def post(self):
#        return {"Why are you moving so fast ?!"}
#
#api.add_resource(Geoposition, '/geoposition/')

if __name__ == '__main__':
    api.run(debug=True)

