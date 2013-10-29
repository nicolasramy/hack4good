# -*- coding: utf-8 -*-

# SQL Alchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import commute4good

import string
from random import random, randint
import config
from datetime import datetime
from faker import Faker


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def createRandomUsers(session, nb_users, coords, radius):
    f = Faker()
    for i in range(nb_users):
        lon = coords['lon'] + radius*(random()-0.5)
        lat = coords['lat'] + radius*(random()-0.5)
        user = commute4good.User()
        user.firstname = f.first_name()
        user.lastname = f.last_name()
        user.pseudo = f.username()
        user.email = f.email()
        user.created_at = datetime.now()
        user.last_accessed_at = datetime.now()
        user.lon = lon
        user.lat = lat
        user.md5_hash = "e10adc3949ba59abbe56e057f20f883e"  # 123456
        user.connected = True
        session.add(user)
        session.commit()

if __name__ == '__main__':
    config.postgre.password="bddvcub"
    
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
    myCoords = {'lon': 48.88, 'lat': 2.33}
    radius = 0.1
    createRandomUsers(session, 10, myCoords, radius)
    connected_users = session.query(commute4good.User).filter_by(connected=True)
    print "Connected users: %d" % connected_users.count()
