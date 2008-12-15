#!/bin/bash

. /etc/profile.d/modules.sh

module load python

cd /usr/local/alogger-ng

python alogger-ng.py $@

