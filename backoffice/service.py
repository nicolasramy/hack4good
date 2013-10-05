# Import core modules
import sys
import os
import json
from optparse import OptionParser

# Import local modules
import config.service as config


# Configure option parser
parser = OptionParser()
parser.add_option("-c", "--workers", dest="workers",
                  help="Workers to run")

# Store value
(options, args) = parser.parse_args()

# Run this as an executable
if __name__ == '__main__':
    if options.workers is None:
        print "Do the job with min workers"
    else:
        if options.workers <= config.workers_min and options.workers >= config.workers_max:
            print "Do some stuff"
        else:
            print "Invalid value for workers, it should be from %d to %d" % (config.workers_min,
                                                                             config.workers_max)
