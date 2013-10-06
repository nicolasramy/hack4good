# -*- coding: utf-8 -*-
import sys
import datetime
import time

from random import random, randint

# SQL Alchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import commute4good

# Faker
from faker import Faker

# Configuration
import config

coords = {'lon': 48.88, 'lat': 2.33}
radius = 0.1

range_badges = 15
range_users = 100
range_tags = 50

step_geolocation = 5
step_user_badges = 3
step_user_tags = 3

if __name__ == '__main__':

    # Bind engine on PostgreSQL
    engine = create_engine("postgresql://%s:%s@%s:%s/%s" % (config.postgres.username,
                                                            config.postgres.password,
                                                            config.postgres.hostname,
                                                            config.postgres.port,
                                                            config.postgres.database
                                                            )
                           )

    # Start session
    Session = sessionmaker(bind=engine)
    session = Session()

    # faker
    f = Faker()

    ##
    # 1. Badges
    # 2. Users
    # 3. Tags
    #
    # 4. Geolocation
    # 5. User Badges
    # 6. User Tags
    ##

    # 1. Badges
    print "Generate %d badges" % range_badges
    t_start = time.time()

    for i in range(range_badges):
        badge = commute4good.Badge()
        badge.name = "Badge %d" % i
        badge.description = "Short description"
        badge.created_at = datetime.datetime.now()
        badge.min_interactions = randint(0, 3)
        session.add(badge)
        session.commit()

    print "Imported in %f seconds" % (time.time() - t_start)

    # 2. Users
    print "Generate %d users" % range_users
    t_start = time.time()

    for i in range(range_users):
        lon = coords['lon'] + radius*(random() - 0.5)
        lat = coords['lat'] + radius*(random() - 0.5)
        user = commute4good.User()
        user.firstname = f.first_name()
        user.lastname = f.last_name()
        user.pseudo = f.username()
        user.email = f.email()
        user.created_at = datetime.datetime.now()
        user.last_accessed_at = datetime.datetime.now()
        user.lon = lon
        user.lat = lat
        user.md5_hash = "e10adc3949ba59abbe56e057f20f883e"  # 123456
        user.connected = True
        session.add(user)
        session.commit()

    print "Imported in %f seconds" % (time.time() - t_start)

    # 3. Tags
    print "Generate %d tags" % range_tags
    t_start = time.time()

    for i in range(range_tags):
        tag = commute4good.Tag()

        lorem = f.lorem()
        tag.name = lorem[0:randint(5, 20)]

        tag.description = "Short description"
        session.add(tag)
        session.commit()

    print "Imported in %f seconds" % (time.time() - t_start)

    # 4. Geolocation
    print "Generate Geolocation"
    t_start = time.time()

    users = session.query(commute4good.User).all()

    for user in users:
        for i in range(randint(1, step_geolocation)):
            lon = coords['lon'] + radius*(random() - 0.5)
            lat = coords['lat'] + radius*(random() - 0.5)

            geolocation = commute4good.Geolocation()
            geolocation.user_id = user.id
            geolocation.lon = lon
            geolocation.lat = lat
            geolocation.created_at = datetime.datetime.now()
            session.add(geolocation)
            session.commit()

    print "Imported in %f seconds" % (time.time() - t_start)

    # 5. User Badges
    print "Generate User Badges"
    t_start = time.time()

    users = session.query(commute4good.User).all()

    for user in users:
        for i in range(randint(1, step_user_badges)):
            user_badge = commute4good.UsersBadge()
            user_badge.user_id = user.id
            user_badge.badge_id = randint(1, range_badges)
            user_badge.earned_at = datetime.datetime.now()
            session.add(user_badge)
            session.commit()

    print "Imported in %f seconds" % (time.time() - t_start)

    # 6. User Tags
    print "Generate User Tags"
    t_start = time.time()

    users = session.query(commute4good.User).all()

    for user in users:
        for i in range(randint(1, step_user_tags)):
            user_tag = commute4good.UsersTag()
            user_tag.user_id = user.id
            user_tag.tag_id = randint(1, range_tags)
            user_tag.add_at = datetime.datetime.now()
            session.add(user_tag)
            session.commit()

    print "Imported in %f seconds" % (time.time() - t_start)
