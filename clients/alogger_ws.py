#! /usr/bin/env python

import xmlrpclib
import datetime
import sys, os
import getopt


MACHINE_NAME = 'brecca-ng'
USERNAME = 'accounts'
PASSWORD = 'BioVae6e'


LOG_DIR = '/usr/spool/PBS/server_priv/accounting'
LOG_TYPE = 'PBS'
url = 'https://%s:%s@www.vpac.org/researchers/accounts/xmlrpc/' % (USERNAME, PASSWORD)


def parse_logs(date):

    filename = date.strftime('%Y%m%d')

    try:
        f = open('%s/%s' % (LOG_DIR, filename), 'r')
    except:
        print 'ERROR: failed to open file %s/%s' % (LOG_DIR, filename)
        sys.exit(1)


    
    data = f.readlines()
    if data:

        server = xmlrpclib.Server(url)


        try:
            summary, output = server.parse_usage(data, str(date), MACHINE_NAME, LOG_TYPE)
            print summary
            
            for line in output:
                print line
                
        except:
            print server.parse_usage(data, str(date), MACHINE_NAME, LOG_TYPE)
            

    
def print_help():
    print 'Usage:'
    print ''
    print '  -h  -  Print help'
    print '  -f  -  Specify log file eg. 20071225'
    print '  -y  -  proccess yesterdays log file'
    print '  -A  -  Read all log files'
    print ''


if __name__ == "__main__":

    opts, args = getopt.getopt(sys.argv[1:], 'yAhf:')
    opts = dict(opts)

    if not opts or '-h' in opts:
        print_help()
        sys.exit(1)


    if '-A' in opts:
        file_list = os.listdir(LOG_DIR)

        for filename in file_list:
            date = datetime.date(int(filename[:4]), int(filename[4:6]), int(filename[6:]))
            parse_logs(date)
        sys.exit(0)
         
        
    if '-f' in opts:
        filename = opts['-f']
        date = datetime.date(int(filename[:4]), int(filename[4:6]), int(filename[6:]))
    elif '-y' in opts:
        date = datetime.date.today() - datetime.timedelta(days=1)
        #date = date.strftime('%Y%m%d')
    else:
        print 'ERROR: You must specify either -f or -y'

    parse_logs(date)

    sys.exit(0)
