# Copyright 2008 VPAC
#
# This file is part of alogger-ng.
#
# alogger-ng is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# alogger-ng is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with alogger-ng  If not, see <http://www.gnu.org/licenses/>.

"""
alogger-ng utils

"""


def print_error(line_no, message):
    """
    Method called when error occurs
    """
    print 'Line: %s --- %s' % (line_no, message)



def get_in_seconds(time):
    """
    Takes a string in format HH:MM:SS
    Note hours can be more than 2 digits

    if greater than 3 years
    
    returns the time in seconds
    """
    hours, minutes, seconds = time.split(':')

    #26280 = 3 years in hours
    if int(hours) > 26280:
        raise ValueError

    total = int( (int(hours)*60*60) + (int(minutes)*60) + int(seconds) )

    return total

