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

from datetime import datetime

from utils import get_in_seconds


def pbs_to_dict(line):
    """
    Parses a PBS log file line into a python dict
    
    raises KeyError when line not valid
    raises ValueError when time over 3 years

    """
    
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
        formatted_data['est_wall_time'] = get_in_seconds(data['Resource_List.walltime'])
        formatted_data['act_wall_time'] = get_in_seconds(data['resources_used.walltime'])
    except:
        raise ValueError
        

    cores = data['exec_host'].count('/')
    formatted_data['cores'] = cores
    formatted_data['cpu_usage'] = cores * formatted_data['act_wall_time']
    
    formatted_data['queue'] = data['queue']

    # Strip kb from end of mem entries
    # No mem field for wembley-hp
    try:
        formatted_data['mem'] = int(data['resources_used.mem'][:len(data['resources_used.mem'])-2])
    except:
        formatted_data['mem'] = 0
    formatted_data['vmem'] = int(data['resources_used.vmem'][:len(data['resources_used.vmem'])-2])
    
    #pmem format 30gb or 400mb also have b and kb
    try:
        pmem_value = int(data['Resource_List.pmem'][:-2])
        pmem_unit = data['Resource_List.pmem'][len(data['Resource_List.pmem'])-2:]
        if units == 'gb':
            formatted_data['list_pmem'] = pmem_value * 1024
        elif units = 'mb':
            formatted_data['list_pmem'] = pmem_value
    except:
        formatted_data['list_pmem'] = 0

    try:
        mem_value = int(data['Resource_List.mem'][:-2])
        mem_unit = data['Resource_List.mem'][len(data['Resource_List.mem'])-2:]
        if units == 'gb':
            formatted_data['list_mem'] = mem_value * 1024
        elif units = 'mb':
            formatted_data['list_mem'] = mem_value
    except:
        formatted_data['list_mem'] = 0 

    try:
        vmem_value = int(data['Resource_List.vmem'][:-2])
        vmem_unit = data['Resource_List.vmem'][len(data['Resource_List.vmem'])-2:]
        if units == 'gb':
            formatted_data['list_vmem'] = vmem_value * 1024
        elif units = 'mb':
            formatted_data['list_vmem'] = vmem_value
    except:
        formatted_data['list_vmem'] = 0 

    try:
        pvmem_value = int(data['Resource_List.pvmem'][:-2])
        pvmem_unit = data['Resource_List.pvmem'][len(data['Resource_List.pvmem'])-2:]
        if units == 'gb':
            formatted_data['list_pvmem'] = pvmem_value * 1024
        elif units = 'mb':
            formatted_data['list_pvmem'] = pvmem_value
    except:
        formatted_data['list_pvmem'] = 0 

    
    formatted_data['exit_status'] = data['Exit_status']


    formatted_data['ctime'] = datetime.fromtimestamp(int(data['ctime'])).isoformat(' ')
    formatted_data['qtime'] = datetime.fromtimestamp(int(data['qtime'])).isoformat(' ')
    formatted_data['etime'] = datetime.fromtimestamp(int(data['etime'])).isoformat(' ')
    formatted_data['start'] = datetime.fromtimestamp(int(data['start'])).isoformat(' ')

    return formatted_data
