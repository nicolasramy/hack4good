# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api
# SQL Alchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import commute4good

import config
from numpy import arccos, arcsin, cos, sin, sqrt, pi
from datetime import datetime

LAT_REF = 48.8
COS_LATITUDE = cos(LAT_REF)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

app = Flask(__name__)
api = Api(app)

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

def to_json(user):
	return jsonify(
		id=user.id,
		firstname=user.firstname, 
		lastname=user.lastname,
		pseudo=user.pseudo,
		email=user.email,
		md5_hash=user.md5_hash,
		photo_path=user.photo_path,
		created_at=user.created_at.strftime(DATE_FORMAT),
		last_accessed_at=user.last_accessed_at.strftime(DATE_FORMAT),
		lat=user.lat,
		lon=user.lon,
		connected=user.connected
		)

class Nearest(Resource):
	# retrieves nearest neighbour
    def get(self, uid):
    	ref_user = session.query(commute4good.User).filter_by(id=int(uid))[0]
    	connected_users = session.query(commute4good.User).filter_by(connected=True)
    	distance = 40000
    	for user in connected_users:
    		latlon1 = [ref_user.lat, ref_user.lon]
    		latlon2 = [user.lat, user.lon]
    		d = distance_GPS(latlon1,latlon2,'linear')
    		if d < distance:
    			nearest_user = user
    			distance = d

    	return to_json(nearest_user)

api.add_resource(Nearest, '/users/nearest/<string:uid>')

class Users(Resource):
	# creates a new user account
	def post(self):
		user = commute4good.User()
		user.firstname = request.form['firstname']
		user.lastname = request.form['lastname']
		user.pseudo = request.form['pseudo']
		user.email = request.form['email']
		user.md5_hash = request.form['md5_hash']
		user.photo_path = request.form['photo_path']
		user.created_at = datetime.now()
		user.last_accessed_at = datetime_now()
		user.lat = request.form['lat']
		user.lon = request.form['lon']
		user.connected = request.form['connected']
		session.add(user)
		session.commit()
		return user.id

	# retrieves infos on user.id = uid
	def get(self, uid):
		user = session.query(commute4good.User).filter_by(id=int(uid))[0]
		return to_json(user)

	# updates infos on user.id = uid
	def put(self, uid):
		user = session.query(commute4good.User).filter_by(id=int(uid))[0]
		session.query(user).update(request.form)
		session.commit()

	# delete user.id = uid
	def delete(self, uid):
		user = session.query(commute4good.User).filter_by(id=int(uid))[0]
		session.delete(user)
		session.commit()

api.add_resource(Users, '/users/<string:uid>')

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
	config.postgre.password = "bddvcub"

	# Bind engine on PostgreSQL
	engine = create_engine("postgresql://%s:%s@%s:%s/%s" % (config.postgre.username,
	                                                        config.postgre.password,
	                                                        config.postgre.hostname,
	                                                        config.postgre.port,
	                                                        config.postgre.database
	                                                        )
	                       )
	
	# Start session
	Session = sessionmaker(bind=engine)
	session = Session()
	connected_users = session.query(commute4good.User).filter_by(connected=True)
	print "Connected users: %d" % connected_users.count()

	app.run(debug=True)
