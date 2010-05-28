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
Declare log parsing methods here.

methods take a line of a log and return a python dict containing

Key           | type     | Description
----------------------------------------------
user          | string   | username
project       | string   | pid
est_wall_time | int      | estimated wall time
act_wall_time | int      | actual wall time
cpu_usage     | int      | CPU usage in seconds
queue         | datetime | 
ctime         | datetime | 
qtime         | datetime | 
etime         | datetime |
start         | datetime |
jobid	      | string   |
cores	      | int      | number of cores
jobname       | string   | Job name
exit_status   | int      | Exit status

Optional
mem           | int      | memory used
vmem          | int      | virtual memory used
list_mem      | int      | memory requested
list_vmem     | int      | virtual memory requested
list_pmem     | int      | memory requested (per processor)
list_pvmem    | int      | virtual memory requested (per processor)

Raises value error if funky wall time

"""

import datetime
import logging

from utils import get_in_seconds


def pbs_to_dict(line):
    """
    Parses a PBS log file line into a python dict
    
    raises KeyError when line not valid
    raises ValueError when time over 3 years

    """
    logging.debug('Parsing line:')
    logging.debug(line)
    # Split line into parts, only care about raw_data
    date, random, job_num, raw_data = line.split(';')
    
    raw_data = raw_data.split(' ')
    
    data = {}
    formatted_data = {}
    
    formatted_data['jobid'] = job_num

    # Make into a dict using values key=value
    for d in raw_data:
        try:
            key, value = d.split('=')
            data[key] = value
        except:
            continue

    # Check to see if line worth proccessing
    if not 'resources_used.walltime' in data:
        raise KeyError


    formatted_data['user'] = data['user']
    if 'account' in data:
        formatted_data['project'] = data['account']

    formatted_data['jobname'] = data['jobname']    
    try:
        formatted_data['act_wall_time'] = get_in_seconds(data['resources_used.walltime'])
    except:
        logging.error('Failed to parse act_wall_time value: %s' % data['resources_used.walltime'])
        raise ValueError
        
    try:
        formatted_data['est_wall_time'] = get_in_seconds(data['Resource_List.walltime'])
    except:
        logging.error('Failed to parse est_wall_time value: %s' % data['Resource_List.walltime'])
        raise ValueError

    formatted_data['exec_hosts'] = [x[:-2] for x in data['exec_host'].split('+')]
    cores = data['exec_host'].count('/')
    formatted_data['cores'] = cores
    formatted_data['cpu_usage'] = cores * formatted_data['act_wall_time']
    
    formatted_data['queue'] = data['queue']

    # Strip kb from end of mem entries
    # No mem field for wembley-hp
    try:
        formatted_data['mem'] = int(data['resources_used.mem'][:len(data['resources_used.mem'])-2])
    except:
        logging.warn('No mem value found')
        formatted_data['mem'] = 0
    formatted_data['vmem'] = int(data['resources_used.vmem'][:len(data['resources_used.vmem'])-2])

    #pmem format 30gb or 400mb also have b and kb
    try:
        pmem_value = int(data['Resource_List.pmem'][:-2])
        pmem_units = data['Resource_List.pmem'][len(data['Resource_List.pmem'])-2:]
        if pmem_units == 'gb':
            formatted_data['list_pmem'] = pmem_value * 1024
        elif pmem_units == 'mb':
            formatted_data['list_pmem'] = pmem_value
    except:
        logging.warn('No list_pmem value found')
        formatted_data['list_pmem'] = 0

    try:
        mem_value = int(data['Resource_List.mem'][:-2])
        mem_units = data['Resource_List.mem'][len(data['Resource_List.mem'])-2:]
        if mem_units == 'gb':
            formatted_data['list_mem'] = mem_value * 1024
        elif mem_units == 'mb':
            formatted_data['list_mem'] = mem_value
    except:
        logging.warn('No list_mem value found')
        formatted_data['list_mem'] = 0 

    try:
        vmem_value = int(data['Resource_List.vmem'][:-2])
        vmem_units = data['Resource_List.vmem'][len(data['Resource_List.vmem'])-2:]
        if vmem_units == 'gb':
            formatted_data['list_vmem'] = vmem_value * 1024
        elif vmem_units == 'mb':
            formatted_data['list_vmem'] = vmem_value
    except:
        logging.warn('No list_vmem value found')
        formatted_data['list_vmem'] = 0 

    try:
        pvmem_value = int(data['Resource_List.pvmem'][:-2])
        pvmem_units = data['Resource_List.pvmem'][len(data['Resource_List.pvmem'])-2:]
        if pvmem_units == 'gb':
            formatted_data['list_pvmem'] = pvmem_value * 1024
        elif pvmem_units == 'mb':
            formatted_data['list_pvmem'] = pvmem_value
    except:
        logging.warn('No list_pvmem value found')
        formatted_data['list_pvmem'] = 0 

    
    formatted_data['exit_status'] = data['Exit_status']

    formatted_data['ctime'] = datetime.datetime.fromtimestamp(int(data['ctime'])).isoformat(' ')
    formatted_data['qtime'] = datetime.datetime.fromtimestamp(int(data['qtime'])).isoformat(' ')
    formatted_data['etime'] = datetime.datetime.fromtimestamp(int(data['etime'])).isoformat(' ')
    formatted_data['start'] = datetime.datetime.fromtimestamp(int(data['start'])).isoformat(' ')

    logging.debug("Parsed following data")
    for k,v in formatted_data.items():
        logging.debug("%s = %s" % (k, v))

    return formatted_data


def sge_to_dict(line):
    """
    Parses a SGE accounting log file line into a python dict
    
    raises KeyError when line not valid
    raises ValueError when time over 3 years

    """
    try:
    
        queue, hostname, group, username, jobname, jobid, account, priority, qsub_time, start_time, end_time, failed, exit_status, ru_wallclock, ru_utime, ru_stime, ru_maxrss, ru_ixrss, ru_ismrss, ru_idrss,  ru_isrss, ru_minflt, ru_majflt, ru_nswap, ru_inblock, ru_oublock, ru_msgsnd, ru_msgrcv, ru_nsignals, ru_nvcsw, ru_nivcsw, project, department, granted_pe, slots, UNKNOWN, cpu, mem, UNKNOWN, command_line_arguments, UNKNOWN, UNKNOWN, maxvmem_bytes = line.split(':')
    except:
        a1, a2, queue, hostname, group, username, jobname, jobid, account, priority, qsub_time, start_time, end_time, failed, exit_status, ru_wallclock, ru_utime, ru_stime, ru_maxrss, ru_ixrss, ru_ismrss, ru_idrss,  ru_isrss, ru_minflt, ru_majflt, ru_nswap, ru_inblock, ru_oublock, ru_msgsnd, ru_msgrcv, ru_nsignals, ru_nvcsw, ru_nivcsw, project, department, granted_pe, slots, UNKNOWN, cpu, mem, UNKNOWN, command_line_arguments, UNKNOWN, UNKNOWN, maxvmem_bytes = line.split(':')

    
    data = {}
    formatted_data = {}
    
    formatted_data['jobid'] = jobid

    formatted_data['date'] = datetime.date.fromtimestamp(long(end_time))
    formatted_data['user'] = username

    formatted_data['jobname'] = jobname 
    try:
        formatted_data['est_wall_time'] = None
        formatted_data['act_wall_time'] = int(ru_wallclock)
    except:
        logging.error('Failed to parse act_wall_time value: %s' % ru_wallclock)
        raise ValueError
        

    formatted_data['cores'] = int(slots)
    formatted_data['cpu_usage'] = formatted_data['cores'] * formatted_data['act_wall_time']
    
    formatted_data['queue'] = queue


    formatted_data['start'] = datetime.date.fromtimestamp(long(qsub_time))
    formatted_data['exit_status'] = exit_status

    logging.debug("Parsed following data")
    for k,v in formatted_data.items():
        logging.debug("%s = %s" % (k, v))

    return formatted_data


