#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.expandvars("../"))

import alogger
print alogger.__file__

from alogger import log_to_dict


fd = open('examples/torque')
lines = fd.readlines()
fd.close()

for line in lines:
    try:
        print log_to_dict(line, 'PBS')
    except KeyError, ValueError:
        pass

