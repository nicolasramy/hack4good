# SQL Alchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import commute4good

import string
from random import random, randint
import config
from datetime import datetime

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def createRandomUsers(session, nb_users, coords, radius):
	firstnames = ['Daffy', 'Mickey', 'Donald', 'Minnie']
	lastnames = ['Duck', 'Mouse', 'Dog', 'Cricket']
	for i in range(nb_users):
		lon = coords['lon'] + radius*(random()-0.5)
		lat = coords['lat'] + radius*(random()-0.5)
		user = commute4good.User()
		user.firstname = firstnames[randint(0,3)]
		user.lastname = lastnames[randint(0,3)]
		user.created_at = datetime.now()
		user.last_accessed_at = datetime.now()
		user.lon = lon
		user.lat = lat
		user.connected = True
		session.add(user)
		session.commit()

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
	myCoords = {'lon':48.88, 'lat':2.33}
	radius = 1.0
	createRandomUsers(session, 10, myCoords, radius)
	connected_users = session.query(commute4good.User).filter_by(connected=True)
	print "Connected users: %d" % connected_users.count()
