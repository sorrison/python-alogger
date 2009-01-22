"""
alogger-ng utils

"""
MAX_JOB_LENGTH = 94608000 # 3 years


"""
Assumes the file name is in the format YYYYMMDD

"""

def log_to_dict(line, LOG_TYPE):
    from alogger_ng.parsers import pbs_to_dict

    if LOG_TYPE == 'PBS':
        return pbs_to_dict(line)

    else:
        raise KeyError


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

