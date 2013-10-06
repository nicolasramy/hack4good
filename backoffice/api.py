# -*- coding: utf-8 -*-
import sys
import datetime

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

    return jsonify(geolocation), 200


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


@api.route('/tags', methods=['POST'])
def new_tag():
    if not request.json or not 'user_id' in request.json or not 'name' in request.json:
        abort(400)

    tag = pg_session.query(commute4good.Tag).filter(commute4good.Tag.name.like("%" + request.json['name'] + "%")).first()

    if tag is None:
        # Create a new Tag
        _tag = commute4good.Tag()
        _tag.name = request.json['name']
        pg_session.add(_tag)
        pg_session.commit()
        tag = _tag

    # TODO: Check existence before save
    # Create jointure
    _user_tag = commute4good.UsersTag()
    _user_tag.user_id = request.json['user_id']
    _user_tag.tag_id = tag.id
    _user_tag.added_at = datetime.datetime.now()
    pg_session.add(_user_tag)
    pg_session.commit()

    data = {
        "id": _user_tag.id,
        "user_id": _user_tag.user_id,
        "tag_id": _user_tag.tag_id,
        "name": tag.name,
        "description": tag.description,
        "popularity": tag.popularity,
        "added_at": _user_tag.added_at
    }

    return jsonify(data), 200

if __name__ == '__main__':
    api.run(debug=True)
