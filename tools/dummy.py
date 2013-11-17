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

# md5 hash
import hashlib

COORDS = {'lon': 48.88, 'lat': 2.33}
RADIUS = 0.1
BASE_DISPLACEMENT = 0.01
TIME_STEP = datetime.timedelta(0,1,0)  # 1 second

RANGE_BADGES = 4
RANGE_USERS = 100
RANGE_TAGS = 100

MAX_GEOLOC_PER_USER = 20
MAX_BADGES_PER_USER = 3
MAX_TAGS_PER_USER = 5

def generate_badges(number):
    print "Generate %d badges" % number
    t_start = time.time()
    fsq_badge_list = [  {"name":"Newbie", "min_inter":1},
                        {"name":"Advanturer", "min_inter":10},
                        {"name":"Explorer", "min_inter":25},
                        {"name":"Socialite", "min_inter":50} ]
    for i in range(number):
        badge = commute4good.Badge()
        badge.name = fsq_badge_list[i]["name"]
        badge.description = fsq_badge_list[i]["name"]
        badge.created_at = datetime.datetime.now()
        badge.min_interactions = fsq_badge_list[i]["min_inter"]
        session.add(badge)
        session.commit()
    print "Imported in %f seconds" % (time.time() - t_start)


def generate_users(number):
    print "Generate %d users" % number
    t_start = time.time()
    # faker
    f = Faker()
    for i in range(number):
        lon = COORDS['lon'] + RADIUS*(random() - 0.5)
        lat = COORDS['lat'] + RADIUS*(random() - 0.5)
        user = commute4good.User()
        user.firstname = f.first_name()
        user.lastname = f.last_name()
        user.pseudo = f.username()
        user.email = f.email()
        user.created_at = datetime.datetime.now()
        user.last_accessed_at = datetime.datetime.now()
        user.lon = lon
        user.lat = lat
        user.md5_pass = hashlib.md5(user.pseudo).hexdigest() # password = pseudo
        user.connected = True
        session.add(user)
    session.commit()
    print "Imported in %f seconds" % (time.time() - t_start)


def generate_tags():
    t_start = time.time()
    # hobby list from wikipedia.en
    hobby_list = ["Amateur radio","Audiophilia","Bboying","Baton twirling",
    "Blogging","Carving wood animals","Chainmail making",
    "Computer programming","Conlanging","Cooking","Coloring","Cosplaying",
    "Crocheting","Creative writing","Dance","Drawing","Fantasy Football",
    "Fishkeeping","Foreign language learning","Gaming","Genealogy",
    "Genetic genealogy","Herpetoculture","Home Movies","Homebrewing",
    "Inline Skating","Jewelry making","Juggling","Knapping","Knitting",
    "Lapidary","Lego Building","Locksport","Magic","Model Railroading",
    "Musical instruments","coco","Ping Pong","Potsdftery","RC cars",
    "Reading","Soapmaking","Skateboarding","Scrapbooking","Sculpting","Sewing",
    "Singing","Taxidermy","Video Gaming","Woodworking","Worldbuilding",
    "Writing","Yoga","Yo-yoing","Air sports","BASE jumping","Beekeeping",
    "Bungee jumping","Bird watching","Board sports","Backpacking","Basketball",
    "Bonsai","Camping","Canoeing","Cosplay","Cycling","Driving","Foraging",
    "Gardening","Geocaching","Ghost Hunting","Graffiti","Golf","Hunting",
    "Hiking","Hooping","Jogging","Kayaking","Kiteboarding","LARPing",
    "Machining","Metal detecting","Motor sports","Mountain biking",
    "Mushroom Hunting","Nordic skating","Parkour","Photography","Rock climbing",
    "Roller skating","Rugby","Running","Sailing","Sand castle building",
    "Rowing","Skiing","Skydiving","Surfing","Swimming","Tai Chi",
    "Urban exploration","Vehicle restoration","Water sports"]
    RANGE_TAGS = len(hobby_list)
    print "Generate %d tags" % RANGE_TAGS
    for i in range(len(hobby_list)):
        tag = commute4good.Tag()
        tag.name = hobby_list[i]
        tag.description = hobby_list[i]
        session.add(tag)
    session.commit()
    print "Imported in %f seconds" % (time.time() - t_start)


def generate_geolocations():
    print "Generate Geolocation"
    t_start = time.time()
    users = session.query(commute4good.User).all()
    for user in users:
        lon = COORDS['lon'] + RADIUS*(2*random() - 1)
        lat = COORDS['lat'] + RADIUS*(2*random() - 1)
        created_at = datetime.datetime.now()
        for i in range(randint(1, MAX_GEOLOC_PER_USER)):
            lon += BASE_DISPLACEMENT*(2*random()-1) # in [-1,1]
            lat += BASE_DISPLACEMENT*(2*random()-1) # in [-1,1]
            created_at -= TIME_STEP*(30+randint(0,30))   # timestep entre 30s et 60s
            geolocation = commute4good.Geolocation()
            geolocation.user_id = user.id
            geolocation.lon = lon
            geolocation.lat = lat
            geolocation.created_at = created_at
            session.add(geolocation)
    session.commit()
    print "Imported in %f seconds" % (time.time() - t_start)


def generate_users_badges():
    print "Generate User Badges"
    t_start = time.time()
    users = session.query(commute4good.User).all()
    for user in users:
        for i in range(randint(1, MAX_BADGES_PER_USER)):           
            user_badge = commute4good.UsersBadge()
            user_badge.user_id = user.id
            user_badge.badge_id = randint(1, RANGE_BADGES)
            user_badge.earned_at = datetime.datetime.now()
            session.add(user_badge)
    session.commit()
    print "Imported in %f seconds" % (time.time() - t_start)

def generate_users_tags():
    print "Generate User Tags"
    t_start = time.time()
    users = session.query(commute4good.User).all()
    for user in users:
        for i in range(randint(1, MAX_TAGS_PER_USER)):
            user_tag = commute4good.UsersTag()
            user_tag.user_id = user.id
            user_tag.tag_id = randint(1, RANGE_TAGS)
            user_tag.add_at = datetime.datetime.now()
            session.add(user_tag)
    session.commit()
    print "Imported in %f seconds" % (time.time() - t_start)

if __name__ == '__main__':

    config.postgres.password="bddvcub"
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

    ##
    # 1. Badges
    # 2. Users
    # 3. Tags
    # 4. Geolocation
    # 5. User Badges
    # 6. User Tags
    ##

    # 1. Badges
    generate_badges(RANGE_BADGES)

    # 2. Users
    generate_users(RANGE_USERS)

    # 3. Tags
    generate_tags()

    # 4. Geolocation
    generate_geolocations()

    # 5. User Badges
    generate_users_badges()

    # 6. User Tags
    generate_users_tags()