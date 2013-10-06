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


@api.route('/users/<int:profil_id>', methods=['GET'])
def user_profil(profil_id):

    user = pg_session.query(commute4good.User).filter_by(id=profil_id).first()

    if user is None:
        return jsonify({"error": "Not found"}), 404

    data = {
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "pseudo": user.pseudo,
        "email": user.email,
        "photo_path": user.photo_path,
        "created_at": user.created_at,
        "last_accessed_at": user.last_accessed_at,
        "lon": user.lon,
        "lat": user.lat,
        "connected": user.connected
    }

    user_badges = pg_session.query(commute4good.UsersBadge).filter_by(user_id=profil_id)
    badges = []
    for user_badge in user_badges:
        badge = pg_session.query(commute4good.Badge).filter_by(id=user_badge.badge_id).first()

        if badge is not None:
            item = {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon_path": badge.icon_path,
                "created_at": badge.icon_path,
                "last_earned_at": badge.last_earned_at,
                "popularity": badge.popularity,
                "min_interactions": badge.min_interactions,
            }
            badges.append(item)

    data["badges"] = badges

    user_tags = pg_session.query(commute4good.UsersTag).filter_by(user_id=profil_id)
    tags = []
    for user_tag in user_tags:
        tag = pg_session.query(commute4good.Tag).filter_by(id=user_tag.tag_id).first()

        if tag is not None:
            item = {
                "id": tag.id,
                "name": tag.name,
                "description": tag.description,
                "popularity": tag.popularity
            }
            tags.append(item)

    data["tags"] = tags

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

