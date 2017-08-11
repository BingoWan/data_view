#!/usr/bin/env python 
#-*-encoding:utf-8-*-

'''
Created on Mar 23, 2017

@author: bingo
'''


import re
import commands
import os
from logger import *
global logName
global logDir
logDir = './logs'
logName = '%s/comand.log'%logDir
os.system('mkdir -p %s'%logDir)
log = Logger(logName, __name__)

def runcmd(cmd):
    pattern = re.compile(r'^rpm.*-i.*|^yum.*install.*')  
    match = pattern.match(cmd)
    matchType = str(type(match)).strip('<|>').split(' ')[1].strip('\'|"')
    if matchType == 'NoneType':
        status, output = commands.getstatusoutput(('%s'%(cmd)))
        if status != 0:
            #errorsymbol = "#"*35+'  ERROR   '+"#"*35
           # log.error("\n%s\n"%errorsymbol)
            log.error("  \" %s \" is not run normally! and exit this program!"%cmd)
            log.error(" COMMAND ERROR %s\n\n"%output)
            if output == '':
                log.error(" COMMAND ERROR :the result is empty!\n\n")
            exit(1)
        else:
            log.info("\"%s\" run perfect"%cmd)
            print color.g("[%s]"%color.B("The result run out by current command:%s"%output))
            return output
    else:
        print("running the \"%s\"....."%cmd)
        os.system(cmd)
