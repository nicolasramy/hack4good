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

# Computes distance
from numpy import arccos, arcsin, cos, sin, sqrt, pi
from datetime import datetime

LAT_REF = 48.8
COS_LATITUDE = cos(LAT_REF)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Flask Application
api = Flask(__name__)

# Specific local password
config.postgres.password = "bddvcub"


def distance_GPS(latlon1, latlon2, method = 'method1', clat = COS_LATITUDE):
    """Take as argument two couples of lat,lon coordinates (tuple or list).
       Return the distance between the points, in km (float).
       Two method are available (the first per default), and a linear method is available too (we consider the area where the points are as a plane).
       This optional method need cos(medium_latitude), medium_latitude is a latitude not so far from the tested points.
    """
    lat1 = latlon1[0]
    lon1 = latlon1[1]
    lat2 = latlon2[0]
    lon2 = latlon2[1]

    if method == 'method1':
        dist_GPS = arccos( sin(lat1*pi/180)*sin(lat2*pi/180) + cos(lat1*pi/180)*cos(lat2*pi/180)*cos(lon1*pi/180-lon2*pi/180) ) * 6366
    
    elif method == 'method2':
        a = sin((lat1*pi/180-lat2*pi/180)/2)
        b = cos(lat1*pi/180) * cos(lat2*pi/180) * sin( (lon1*pi/180- lon2*pi/180)/2 )
        dist_GPS = 2*arcsin( sqrt( a**2 + b**2 )) * 6366

    elif method == 'linear':
        dist_GPS = sqrt(((111.1*(lat2-lat1))**2)+((111.1*clat*(lon2-lon1))**2))

    return dist_GPS

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

    # TODO: Check User
    # Create jointure
    geoposition = commute4good.Geoposition()
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

    geolocation = {
        "user_id": request.json['user_id'],
        "lon": request.json['lon'],
        "lat": request.json['lat']
    }

    # Save

    return jsonify(geolocation), 200


@api.route('/users/nearest/<int:profile_id>', methods=['GET'])
def nearest_neighbour(profile_id):

    max_distance = 1.0          # return users closer than 1000m
    max_returned_users = 50     # return at max 50 users

    ref_user = pg_session.query(commute4good.User).filter_by(id=profile_id).first()

    if ref_user is None:
        return jsonify({"error": "Not found"}), 404

    connected_users = pg_session.query(commute4good.User).filter_by(connected=True)
    data = {}
    neighbours = []
    for user in connected_users:
        latlon1 = [ref_user.lat, ref_user.lon]
        latlon2 = [user.lat, user.lon]
        d = distance_GPS(latlon1,latlon2,'linear')
        # d > 1m to avoid returning the requesting user itself
        if d < max_distance and d > 0.001:  
            # a good thing to stringify every field to avoid returning a postgres
            # keyword when field is eg. 'null' or 'true'
            item = {
                "id": str(user.id),
                "firstname": str(user.firstname),
                "lastname": str(user.lastname),
                "pseudo": str(user.pseudo),
                "email": str(user.email),
                "photo_path": str(user.photo_path),
                "created_at": str(user.created_at.strftime(DATE_FORMAT)),
                "last_accessed_at": str(user.last_accessed_at.strftime(DATE_FORMAT)),
                "lon": str(user.lon),
                "lat": str(user.lat),
                "connected": str(user.connected),
                "distance_km": str(d)
            }
            neighbours.append(item)

    data['nearest_neighbours'] =  sorted(neighbours,
        key=lambda neighbour: neighbour['distance_km'])[:max_returned_users]

    return jsonify(data)

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

@api.route('/users', methods=['POST'])
def new_user():
    new_user = commute4good.User()
    pg_session.add(new_user)
    pg_session.commit()
    _user_id = new_user.id
    try:
        if request.json['firstname'] != "":
            new_user.firstname = request.json['firstname']
    except Exception:
        pass

    try:
        if request.json['lastname'] != "":
            new_user.firstname = request.json['lastname']
    except Exception:
        pass

    try:
        if request.json['pseudo'] != "":
            new_user.firstname = request.json['pseudo']
    except Exception:
        pass

    try:
        if request.json['email'] != "":
            new_user.firstname = request.json['email']
    except Exception:
        pass

    try:
        if request.json['md5_hash'] != "":
            new_user.firstname = request.json['md5_hash']
    except Exception:
        pass

    try:
        if request.json['photo_path'] != "":
            new_user.firstname = request.json['photo_path']
    except Exception:
        pass

    new_user.created_at = datetime.now()
    new_user.last_accessed_at = datetime.now()

    pg_session.add(new_user)
    pg_session.commit()

    return "yo new user " + str(_user_id) + " !"

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
