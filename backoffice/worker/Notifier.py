# -*- coding: utf-8 -*-

# Core modules
import sys
import multiprocessing
from numpy import cos, sin, arccos, arcsin, sqrt, pi

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import commute4good

# Custom modules
import config

LAT_REF = 48.833
COS_LATITUDE = cos(LAT_REF)


# Default function to do the job
def run(processing_concurrency=config.service.workers_min):

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

    # Retrieve connected users
    users = session.query(commute4good.User).filter_by(connected=True)

    # Create a queue for data to be inserted in a multiprocessing pool
    try:
        pool = multiprocessing.Pool(processes=processing_concurrency)
        pool.map(subworker, users)

        # Prevents any more tasks from being submitted to the pool.
        # Once all the tasks have been completed the worker processes will exit.
        pool.close()

        # Stops the worker processes immediately without completing outstanding work.
        # When the pool object is garbage collected terminate() will be called immediately.
        #pool.terminate()

        # Wait for the worker processes to exit. One must call close() or terminate() before using join().
        pool.join()

    except KeyboardInterrupt:
        sys.exit(1)

    except Exception as error:
        print str(error)
        sys.exit(1)

    return True


def subworker(user):
    # Do some stuff
    user_position = [user.lon, user.lat]

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

    connected_users = session.query(commute4good.User).filter(commute4good.User.connected == True,
                                                              commute4good.User.id != user.id)

    for neighbor in connected_users:
        neighbor_position = [neighbor.lon, neighbor.lat]
        distance = distance_GPS(user_position, neighbor_position, method="linear")

        if distance <= 0.1:
            print "User %s is nearest to %s" % (user.pseudo, neighbor.pseudo)
            print "Send notification"

    session.close()
    engine.dispose()


def distance_GPS(latlon1, latlon2, method='standard', clat=COS_LATITUDE):
    """Take as argument two couples of lat,lon coordinates (tuple or list).
       Return the distance between the points, in km (float).
       Two method are available (the first per default), and a linear method is available too (we consider the area where the points are as a plane).
       This optional method need cos(medium_latitude), medium_latitude is a latitude not so far from the tested points.
    """
    lat1 = latlon1[0]
    lon1 = latlon1[1]
    lat2 = latlon2[0]
    lon2 = latlon2[1]

    if method == 'standard':
        dist_GPS = arccos(sin(lat1 * pi/180) * sin(lat2 * pi/180)
                          + cos(lat1 * pi/180) * cos(lat2 * pi/180)
                          * cos(lon1 * pi/180 - lon2 * pi/180)) * 6366

    elif method == 'alternative':
        a = sin((lat1 * pi/180 - lat2 * pi/180)/2)
        b = cos(lat1 * pi/180) * cos(lat2 * pi/180) * sin((lon1*pi/180 - lon2*pi/180)/2)
        dist_GPS = 2 * arcsin(sqrt(a ** 2 + b ** 2)) * 6366

    elif method == 'linear':
        dist_GPS = sqrt(((111.1 * (lat2-lat1)) ** 2) + ((111.1 * clat * (lon2 - lon1)) ** 2))

    return dist_GPS
