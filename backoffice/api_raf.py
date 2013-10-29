# -*- coding: utf-8 -*-
import sys
import datetime
import json
import urllib2

# Flask
from flask import Flask, request, jsonify, make_response, abort

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Computes distance
from numpy import arccos, arcsin, cos, sin, sqrt, pi

# commute4good
import config
from model import commute4good

LAT_REF = 48.8
COS_LATITUDE = cos(LAT_REF)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
API_KEY = "AIzaSyDPIJ60O2lESkHR6DjKru8G3uFpg1xkUzs"

# Flask Application
api = Flask(__name__)


@api.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid data'}), 400)


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

config.postgres.password = "bddvcub"

# Bind engine - postgresql
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

#########################################################
#   USEFUL METHODS
#########################################################
def date_tostring(date):
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    try:
        s = date.strftime(DATE_FORMAT)
    except Exception, e:
        s = None
    return s

#########################################################
#   GEOLOCATION METHODS
#########################################################
@api.route('/geolocation2/<string:str>', methods=['GET'])
def geolocation2(str):
    params = str.split("-")
    # Check User
    uid = params[0]
    lat = params[1]
    lon = params[2]
    user = pg_session.query(commute4good.User).filter_by(id=uid).first()
    if user is None:
        return jsonify({"error": "Not found2"}), 403

    # Update user position
    user.lon = lon
    user.lat = lat
    user.last_accessed_at = datetime.datetime.now()
    pg_session.add(user)
    pg_session.commit()

    # Create log
    geolocation = commute4good.Geolocation()
    geolocation.user_id = user.id
    geolocation.lon = lon
    geolocation.lat = lat
    geolocation.created_at = datetime.datetime.now()
    pg_session.add(geolocation)
    pg_session.commit()

    # Prepare response data
    data = geolocation.to_dict()

    # Send jsonified data as response
    return jsonify(data), 200


@api.route('/geolocation', methods=['POST'])
def new_position():
    if not request.json or not 'user_id' in request.json or not 'lon' in request.json or not 'lat' in request.json:
        abort(400)

    # Check User
    uid = int(request.json['user_id'])
    user = pg_session.query(commute4good.User).filter_by(id=int(request.json['user_id'])).first()
    if user is None:
        return jsonify({"error": "Not found2"}), 403

    # Update user position
    user.lon = request.json['lon']
    user.lat = request.json['lat']
    user.last_accessed_at = datetime.datetime.now()
    pg_session.add(user)
    pg_session.commit()

    # Create log
    geolocation = commute4good.Geolocation()
    geolocation.user_id = user.id
    geolocation.lon = request.json['lon']
    geolocation.lat = request.json['lat']
    geolocation.created_at = datetime.datetime.now()
    pg_session.add(geolocation)
    pg_session.commit()

    # Prepare response data
    data = geolocation.to_dict()

    # Send data jsonified as response
    return jsonify(data), 200


###########################################################
#   USERS METHODS :
#       GET USER INFOS      : /users/<int>          GET
#       CREATE NEW USER     : /users                POST
#       UPDATE USER         : /users                PUT
#       LOG IN USER         : /users/login          POST
#       GET NEAREST USERS   : /users/nearest/<int>  GET 
###########################################################

#   GET USER INFOS
@api.route('/users/<int:profil_id>', methods=['GET'])
def user_profil(profil_id):
    """
    Return infos concerning user 'profil_id' in a json string, including his 
    badges and tags
    """

    # Check User
    user = pg_session.query(commute4good.User).filter_by(id=profil_id).first()
    if user is None:
        return jsonify({"error": "Not found"}), 404

    # Prepare response data
    data = user.to_dict()

    # Badges
    user_badges = pg_session.query(commute4good.UsersBadge).filter_by(user_id=profil_id)
    badges = []
    for user_badge in user_badges:
        badge = pg_session.query(commute4good.Badge).filter_by(id=user_badge.badge_id).first()

        if badge is not None:
            item = badge.to_dict()
            badges.append(item)

    data["badges"] = badges

    # Tags
    user_tags = pg_session.query(commute4good.UsersTag).filter_by(user_id=profil_id)
    tags = []
    for user_tag in user_tags:
        tag = pg_session.query(commute4good.Tag).filter_by(id=user_tag.tag_id).first()

        if tag is not None:
            item = tag.to_dict()
            tags.append(item)

    data["tags"] = tags

    # Send data jsonified as response
    return jsonify(data)


#   CREATE USER   
@api.route('/users', methods=['POST'])
def new_user():
    """
    Creates a new user using post data
    """
    user = commute4good.User()
    pg_session.add(user)
    pg_session.commit()
    _user_id = user.id

    # Set fields if they are not empty
    try:
        if request.json['firstname'] != "":
            user.firstname = request.json['firstname']
    except Exception:
        pass
    try:
        if request.json['lastname'] != "":
            user.lastname = request.json['lastname']
    except Exception:
        pass
    try:
        if request.json['pseudo'] != "":
            user.pseudo = request.json['pseudo']
    except Exception:
        pass
    try:
        if request.json['email'] != "":
            user.email = request.json['email']
    except Exception:
        pass
    try:
        if request.json['md5_pass'] != "":
            user.md5_pass = request.json['md5_pass']
    except Exception:
        pass
    try:
        if request.json['photo_b64'] != "":
            user.photo_b64 = request.json['photo_b64']
    except Exception:
        pass
    try:
        if request.json['lat'] != "":
            user.lat = request.json['lat']
    except Exception:
        pass
    try:
        if request.json['lon'] != "":
            user.lon = request.json['lon']
    except Exception:
        pass
    try:
        if request.json['connected'] != "":
            user.connected = request.json['connected']
    except Exception:
        pass
    try:
        if request.json['gcm_reg_id'] != "":
            user.gcm_reg_id = request.json['gcm_reg_id']
    except Exception:
        pass

    user.created_at = datetime.datetime.now()
    user.last_accessed_at = datetime.datetime.now()

    pg_session.add(user)
    pg_session.commit()

    # Prepare response data
    data = user.to_dict()

    return jsonify(data)


#   UPDATE USER DATA
@api.route('/users', methods=['PUT'])
def update_user():
    """
    Updates an existing user with PUT data
    """
    if not request.json or not 'user_id' in request.json:
        abort(400)

    user = pg_session.query(commute4good.User).filter_by(id=request.json['user_id']).first()

    if user is None:
        return jsonify({"error": "Not found"}), 403

    # TODO: Check user authorization -> 403 on failure

    # Update fields if they are not empty
    try:
        if request.json['firstname'] != "":
            user.firstname = request.json['firstname']
    except Exception:
        pass
    try:
        if request.json['lastname'] != "":
            user.lastname = request.json['lastname']
    except Exception:
        pass
    try:
        if request.json['pseudo'] != "":
            user.pseudo = request.json['pseudo']
    except Exception:
        pass
    try:
        if request.json['email'] != "":
            user.email = request.json['email']
    except Exception:
        pass
    try:
        if request.json['md5_pass'] != "":
            user.md5_pass = request.json['md5_pass']
    except Exception:
        pass
    try:
        if request.json['photo_b64'] != "":
            user.photo_b64 = request.json['photo_b64']
    except Exception:
        pass
    try:
        if request.json['lat'] != "":
            user.lat = request.json['lat']
    except Exception:
        pass
    try:
        if request.json['lon'] != "":
            user.lon = request.json['lon']
    except Exception:
        pass
    try:
        if request.json['connected'] != "":
            user.connected = request.json['connected']
    except Exception:
        pass
    try:
        if request.json['gcm_reg_id'] != "":
            user.gcm_reg_id = request.json['gcm_reg_id']
    except Exception:
        pass

    user.last_accessed_at = datetime.datetime.now()

    pg_session.add(user)
    pg_session.commit()

    # Prepare response data
    data = user.to_dict()

    # Send data jsonified as response
    return jsonify(data)


#   LOGIN USER
@api.route('/users/login', methods=['POST'])
def create_token():
    # Check User identification
    if not request.json or not 'pseudo' in request.json or not 'md5_pass' in request.json:
        abort(400)

    # Search user
    user = pg_session.query(commute4good.User).filter_by(pseudo=request.json['pseudo'],
                                                         md5_pass=request.json['md5_pass']).first()

    # User not found
    if user is None:
        return jsonify({"error": "Not found"}), 403

    # Update last connection log
    user.last_accessed_at = datetime.datetime.now()
    pg_session.add(user)
    pg_session.commit()

    # Prepare response data
    data = user.to_dict()

    # Send data jsonified as response
    return jsonify(data)


#   GET NEAREST NEIGHBORS METHODS
@api.route('/users/nearest/<int:profile_id>', methods=['GET'])
def nearest_neighbour(profile_id):
    """
    Return nearest neighbours of user 'profile_id'

    Returns only :
        a maximum of MAX_RETURNED_USERS
        users that are closer than MAX_DISTANCE
    """

    MAX_DISTANCE = 1.0          # return users closer than 1000m
    MAX_RETURNED_USERS = 10     # return at max 10 users
    GET_FRIENDS_FIRST = False

    ref_user = pg_session.query(commute4good.User).filter_by(id=profile_id).first()

    if ref_user is None:
        return jsonify({"error": "Not found"}), 404

    connected_users = pg_session.query(commute4good.User).filter_by(connected=True)
    data = {}
    neighbours = []
    for user in connected_users:
        latlon1 = [ref_user.lat, ref_user.lon]
        latlon2 = [user.lat, user.lon]
        d = distance_GPS(latlon1, latlon2, 'linear')
        # d > 10cm to avoid returning the requesting user itself
        if d < MAX_DISTANCE and d > 0.0001:
            user_tags = get_user_tags(user)
            item = user.to_dict()
            item['distance_km'] = d 
            item['user_tags'] = user_tags
            neighbours.append(item)

    data['nearest_neighbours'] = sorted(neighbours, key=lambda neighbour: neighbour['distance_km'])[:MAX_RETURNED_USERS]
    return jsonify(data)


####################################################
#   CREATE TAGS METHODS
####################################################
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
    user_tag = commute4good.UsersTag()
    user_tag.user_id = request.json['user_id']
    user_tag.tag_id = tag.id
    user_tag.added_at = datetime.datetime.now()
    pg_session.add(user_tag)
    pg_session.commit()

    # Prepare response data
    data = {
        "id": user_tag.id,
        "user_id": user_tag.user_id,
        "tag_id": user_tag.tag_id,
        "name": tag.name,
        "description": tag.description,
        "popularity": tag.popularity,
        "added_at": date_tostring(user_tag.added_at)
    }

    # Send data jsonified as response
    return jsonify(data), 200


######################################################################
#   PRIVATE MESSAGES METHODS
#       GET LATEST MESSAGES : /private-chat/<int>       GET
#       POST NEW MESSAGE    : /private-chat/            POST
######################################################################
#   GET LATEST MESSAGES
@api.route('/private-chat/<int:chat_id>', methods=['GET'])
def latest_privatechat_messages(chat_id):
    MAX_RETURNED_MESSAGES = 50

    pms = pg_session.query(commute4good.PrivatechatsMessage).filter_by(privatechat_id=chat_id)

    if pms is None:
        return jsonify({"error": "No private chat with this id"}), 403

    # TODO: Check user authorization -> 403 on failure

    # Retrieve all messages from the given private chat
    data = {}
    messages = []
    for pm in pms:
        item = pm.to_dict()
        messages.append(item)

    data['latest_messages']=messages
    #data['latest_privatechat_messages'] = sorted(messages, key=lambda message: message['created_at'], reverse=True)[:MAX_RETURNED_MESSAGES]
    return jsonify(data) 

#   POST NEW MESSAGE
@api.route('/private-chat', methods=['POST'])
def new_privatechat_message():
    """
    Creates a new pr_mess using post data
    """
    if not request.json or not 'privatechat_id' in request.json:
        abort(400)

    pr_mess = commute4good.PrivatechatsMessage()
    pg_session.add(pr_mess)
    pg_session.commit()
    _pr_mess_id = pr_mess.id

    # Set fields if they are not empty
    try:
        if request.json['privatechat_id'] != "":
            pr_mess.privatechat_id = request.json['privatechat_id']
    except Exception:
        pass
    try:
        if request.json['sender_id'] != "":
            pr_mess.sender_id = request.json['sender_id']
    except Exception:
        pass
    try:
        if request.json['content'] != "":
            pr_mess.content = request.json['content']
    except Exception:
        pass
    try:
        if request.json['lat'] != "":
            pr_mess.lat = request.json['lat']
    except Exception:
        pass
    try:
        if request.json['lon'] != "":
            pr_mess.lon = request.json['lon']
    except Exception:
        pass

    pr_mess.created_at = datetime.datetime.now()

    pg_session.add(pr_mess)
    pg_session.commit()

    # Prepare response data
    data = pr_mess.to_dict()

    return jsonify(data)



###############################################################
#   SEND NOTIFICATION METHODS
###############################################################
@api.route('/notification2/<int:receiver_id>', methods=['GET'])
# GET method where only the receiver_id is used
def notification2(receiver_id):
    if receiver_id == 8:
        regId = "APA91bFjTwhIKqpMrfkItWIn8RHbA3HHHvGjdhs8iRURQ3n2SY6cV30cPw2-CEfAjLWFgYpTc57-X4t2PLXec2ZLGQs2kxTPNejqBrWumOdzHvqZT9qbuo9Y4JFqcROa5dVSMduRxpC9qQtZpdtmV4WanOllaLej6b8Z5ZbklFCQ9m3pe9hUc30"
        pseudo = "Iva"
    if receiver_id == 9:
        regId = "APA91bG6Gc4l753AzdAaAUUGvxY_dsXQJJbI78Qtq7K0VCjrxSEQL3ubfgL-iTHqzHlk5362qTaZrQi-kSb9Nyd6aNr3xzapSFcJA-K3qUYk-_TuwNgMTwpdtZIACNJAvgUMzZZqN_EAooMmXLSDkNUAeGhIhTV2xw"
        pseudo = "Martine"
    
    message = pseudo+ " would like to meet you"

    # send notification to receiver
    send_notification(regId, message)
    
    return "yo notification2"

@api.route('/notification3/<string:str>', methods=['GET'])
# GET method where both sender_id and receiver_id are used
def notification3(str):
    params = str.split("-")
    sender_id = params[0]
    receiver_id = params[1]

    # Search users
    sender = pg_session.query(commute4good.User).filter_by(id=sender_id.first())
    receiver = pg_session.query(commute4good.User).filter_by(id=receiver_id.first())

    if receiver_id == 8:
        regId = "APA91bFjTwhIKqpMrfkItWIn8RHbA3HHHvGjdhs8iRURQ3n2SY6cV30cPw2-CEfAjLWFgYpTc57-X4t2PLXec2ZLGQs2kxTPNejqBrWumOdzHvqZT9qbuo9Y4JFqcROa5dVSMduRxpC9qQtZpdtmV4WanOllaLej6b8Z5ZbklFCQ9m3pe9hUc30"
    if receiver_id == 9:
        regId = "APA91bG6Gc4l753AzdAaAUUGvxY_dsXQJJbI78Qtq7K0VCjrxSEQL3ubfgL-iTHqzHlk5362qTaZrQi-kSb9Nyd6aNr3xzapSFcJA-K3qUYk-_TuwNgMTwpdtZIACNJAvgUMzZZqN_EAooMmXLSDkNUAeGhIhTV2xw"

    pseudo = sender.pseudo
    message = pseudo + " would like to meet you"

    # send notification to receiver
    send_notification(regId, message)
    
    return "yo notification2"


@api.route('/notification', methods=['POST'])
def notification():
    # Check User identification
    if not request.json or not 'sender_id' in request.json or not 'receiver_id' in request.json:
        abort(400)

    # Search users
    sender = pg_session.query(commute4good.User).filter_by(id=int(request.json['sender_id'])).first()
    receiver = pg_session.query(commute4good.User).filter_by(id=int(request.json['receiver_id'])).first()

     # User not found
    if receiver is None:
        return jsonify({"error": "Not found"}), 403

    #regId = receiver.regId
    regId = "APA91bFjTwhIKqpMrfkItWIn8RHbA3HHHvGjdhs8iRURQ3n2SY6cV30cPw2-CEfAjLWFgYpTc57-X4t2PLXec2ZLGQs2kxTPNejqBrWumOdzHvqZT9qbuo9Y4JFqcROa5dVSMduRxpC9qQtZpdtmV4WanOllaLej6b8Z5ZbklFCQ9m3pe9hUc30"
    message = sender.pseudo + " would like to meet you"

    # send notification to receiver
    result = send_notification(regId, message)

    # add in database

    mr = commute4good.MeetingRequest()
    mr.accepted = False
    mr.receiver_lat = receiver.lat
    mr.sender_lat = sender.lat
    mr.sent_at = datetime.datetime.now()               
    mr.receiver_id = receiver.id
    mr.receiver_lon = receiver.lon
    mr.sender_id = sender.id
    mr.sender_lon = sender.lon  
    pg_session.add(mr)
    pg_session.commit()

    return "todo"


def send_notification(regId, message):
    # sends a push notification to Google Cloud Messaging
    json_data = {"data" : {
                    "message" : message
               }, "registration_ids": [regId],
    }

    url = 'https://android.googleapis.com/gcm/send'
    myKey = "key=" + API_KEY
    data = json.dumps(json_data)
    headers = {'Content-Type': 'application/json', 'Authorization': myKey}
    req = urllib2.Request(url, data, headers)
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
   
    return response

def get_user_tags(user):
    # Create jointure
    user_tags = pg_session.query(commute4good.UsersTag).filter_by(user_id=user.id)[0:3]
    
    tag_names=[]
    for user_tag in user_tags:
        tag = pg_session.query(commute4good.Tag).filter_by(id=user_tag.tag_id).first()
        tag_names.append(tag.name)

    return tag_names

def distance_GPS(latlon1, latlon2, method='method1', clat=COS_LATITUDE):
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

# Run as an executable
if __name__ == '__main__':
    api.run(debug=True)
