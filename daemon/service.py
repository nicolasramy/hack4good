# -*- coding: utf-8 -*-
# Import core modules
from optparse import OptionParser
import time

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
        while 1:
            worker.Notifier.run(config.service.workers_min)
            time.sleep(60)

    else:
        workers = int(options.workers)

        if workers >= config.service.workers_min and workers <= config.service.workers_max:
            while 1:
                worker.Notifier.run(workers)
                time.sleep(60)

        else:
            print "Invalid value for workers, it should be from %d to %d" % (config.service.workers_min,
                                                                             config.service.workers_max)
