#!/usr/bin/env python
#-*-encoding:utf-8-*-
# @Author: Bingo Wan <bingo>
# @Date:   2017-06-04T21:09:53+08:00
# @Email:  wanwuko@gmail.com
# @Last modified by:   bingo
# @Last modified time: 2017-06-18T22:43:44+08:00
# @Copyright: The full copyright is belong to Bingo Wan

"""
Given a presto server host and an option time range.
Options:
--h get hte help information
-h <query host>   host for presto server host
-f <day_start>    From day time for query
-t <day_end>      To day time for query
Comand example:
./cpuload.py -f 6/1 -t 6/7
"""

import re
import sys
import datetime
from wlibs.tools import *
import numpy as np
import getopt
import inspect
import textwrap
import threading
import calendar


def stanDeviation(data):
    sum = 0
    for i in range(len(data)):
        sum += data[i]
    avg = sum/len(data)
    sum_dev = 0
    for d in data:
        Devi = d - avg
        sum_dev += Devi**2
    result = np.sqrt(sum_dev/len(data))
    return result



def getHost(flag):
    with open('./hosts') as files:
        hostlist = []; typelist = []
        f = files.readlines()
        for data in f:
            raw = re.split(' ',data)
            typehost = raw[0]
            host = raw[-1].strip('\n')
            typelist.append(typehost)
            hostlist.append(host)
        if flag == 'host':
            return hostlist
        if flag == 'type':
            return

def writedata(hosts):
    for host in hosts:
        cmd_host = "echo \"select cpu_usage from com_cnc_gdp_mdio_wsms_par.cpu where host=%s  and m=4 and d=%d group by collect_time order by collect_time limit 10;\" > tmp.sql"%(h,day)
        runcmd(cmd_host, alarmoff=True)
        cmd = 'presto-cli --server jydx96:52000 --catalog hive -f tmp.sql > %d_host'%count
        runcmd(cmd, alarmoff=True)
        count += 1


def do_query(month, day_start, day_end, query_host):
    bingo = {}; raw_data = []
    hostlist = getHost('host')
    def highLoad(data): #count the percent of high load in a day data(1440 data point)
        count = 0; value = 1
        for i in range(len(data)):
            if data[i] > value:
                count += 1
        percent = count/float(len(data))
        return percent
    for host in hostlist[:5]:
        sigmaset = []
        for day in range(day_start, day_end):
            cmd2 = "echo \"select av_load from com_cnc_gdp_mdio_wsms_par.load where monitor=\'%s\' and m=%s and d=%s  order by collect_time;\" > sql/tmp_%s.sql"%(host, month, day_start, day_start)
            runcmd(cmd2, alarmoff=False)
            cmd = 'presto-cli --server %s:52000 --catalog hive -f tmp.sql'%query_host
            data = runcmd(cmd, alarmoff=False).replace('\"','').split('\n')
            if len(data) >1:
                try:
                    dataset = [float(d) for d in data]
                    sigma = highLoad(dataset)
                    sigmaset.append((day, sigma))
                    raw_data.append(sigma)
                except ValueError:
                    continue

        bingo[host] = sigmaset
    hosts = []
    files = open('./result_%s'%day_start, 'w')
    for raw in sorted(raw_data, reverse=True)[:20]:
        for key, value in bingo.items():
            count = 0
            if len(value) > 0:
                for data1 in value:
                    count += 1
                    if data1[1] == raw:
                        files.write('%s  %s  %s\n'%(key, data1[0], data1[1]))
                        hosts.append(key)
                        break;

def cleantmpfile():
    cmd = 'rm -rf sql/*'
    runcmd(cmd)

def usage():
    doc = inspect.getmodule(usage).__doc__   #get doc from module which contains object usage
    print >>sys.stderr, textwrap.dedent(doc) # write the usage message into sys.stderr and the color is red.


def main(argv=None):
    try:
        opts, args = getopt.getopt(argv[1:], 'h:f:t:',  ["auto", "help", "test="])
        #print opts, args   #The return value consists of two elements: the first is a list of (option, value) pairs; the second is the list of program arguments left after the option list was stripped (this is a trailing slice of the first argument).  Each option-and-value pair returned has the option as its first element, prefixed with a hyphen (e.g.,'-x'), and the option argument as its second element, or an empty string if the option has no argument.
    except getopt.GetoptError, err:
        print >> sys.stderr, err
        usage()
        return -1
    for option, val in opts:
        if option == '-f':
            month = re.split('/', val)[0]
            monthrange = calendar.monthrange(2017, int(month))[-1]
            day_start = int(re.split('/', val)[1])
        elif option == '-t':
            day_end = int(re.split('/', val)[1])
        elif option == '-h':
            query_host = val
            print query_host
        elif option == '--h':
            usage()
    if len(opts) == 3:
        count = 1
        threads = []
        day = day_start
        while True:
            if count > 7:
                break
            if day > monthrange:
                month += 1
                day_start = 1
            threads.append(threading.Thread(target=do_query,args=(month, day-1, day, query_host,)))
            #do_query(month, daystart, dayend, query_host)
            day += 1
            count += 1
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        return 0
    else:
        usage()
        return -1
    cleantmpfile()
if __name__ == "__main__":
    sys.exit(main(sys.argv))
