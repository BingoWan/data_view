#!/usr/bin/env python 
#-*-encoding:utf-8-*-

'''
Created on May 4, 2017

@author: bingo
'''

import re
import datetime
from wlibs.tools import *
import numpy as np
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
    
def highLoad(data): #count the percent of high load in a day data(1440 data point)
    count = 0; value = 0.8
    for i in range(len(data)):
        if data[i] > value:
            count += 1
    percent = count/float(len(data))
    return percent
    
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
        
        
def func():
    bingo = {}; raw_data = []
    hostlist = getHost('host')
    for host in hostlist:
        sigmaset = []
        for day in range(27, 28):
            cmd2 = "echo \"select av_load from com_cnc_gdp_mdio_wsms_par.load where monitor=\'%s\' and m=7 and d=%d  order by collect_time;\" > tmp.sql"%(host,day)
            runcmd(cmd2, alarmoff=True)
            cmd = 'presto-cli --server jy2x10:52000 --catalog hive -f tmp.sql'
            data = runcmd(cmd, alarmoff=True).replace('\"','').split('\n')
            if len(data) >1:
                dataset = [float(d) for d in data]
                sigma = highLoad(dataset)
                sigmaset.append((day, sigma))
                raw_data.append(sigma)
        bingo[host] = sigmaset
    hosts = []
    files = open('./result', 'w')
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
func()
