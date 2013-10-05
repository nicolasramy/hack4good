# -*- coding: utf-8 -*-
# Import core modules
from optparse import OptionParser

# Import local modules
import config
import worker


# Configure option parser
parser = OptionParser()
parser.add_option("-c", "--workers", dest="workers",
                  help="Workers to run")

# Store value
(options, args) = parser.parse_args()

# Run this as an executable
if __name__ == '__main__':
    if options.workers is None:
        worker.Notifier.run(config.service.workers_min)
    else:
        if options.workers <= config.service.workers_min and options.workers >= config.service.workers_max:
            worker.Notifier.run(options.workers)
        else:
            print "Invalid value for workers, it should be from %d to %d" % (config.service.workers_min,
                                                                             config.service.workers_max)
