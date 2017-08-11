# @Author: Bingo Wan <bingo>
# @Date:   2017-05-22T15:06:52+08:00
# @Email:  wanwuko@gmail.com
# @Last modified by:   bingo
# @Last modified time: 2017-05-22T16:22:10+08:00
# @Copyright: The full copyright is belong to Bingo Wan

import time
import os
import re

def readdata():
    with open('xf1raw.dat') as files:
        fw = open('xf1.dat','w')
        f = files.readlines()
        deltalist = []; count = 1; count1 = 1; sum_delta = 0; i = 1
        for data in f:
            d = re.split(' ', data)[-1].strip('\n')
            if count > 1:
                data_new = int(d)
                delta = data_new - tmp
                #print delta
                #deltalist.append(delta)
                sum_delta += delta
                print data_new, tmp
                if count1 %  60 == 0:
                    print("%s  %s\n"%(i, sum_delta/60))
                    fw.write("%s  %s\n"%(i, sum_delta/60))
                    sum_delta = 0
                    i += 1
            tmp = int(d)
            count += 1
            count1 += 1


readdata()
