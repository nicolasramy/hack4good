# -*- coding: utf-8 -*-

# Core modules
import sys
import multiprocessing

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import commute4good

# Custom modules
import config


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

    connected_users = session.query(commute4good.User).filter_by(connected=True)

    print "Connected users: %d" % connected_users.count()
    sys.exit(1)

    for user in connected_users:
        print user
    sys.exit(1)

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


def subworker(data):
    # Do some stuff
    print data
