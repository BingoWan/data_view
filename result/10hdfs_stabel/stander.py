# @Author: Bingo Wan <bingo>
# @Date:   2017-05-22T19:32:49+08:00
# @Email:  wanwuko@gmail.com
# @Last modified by:   bingo
# @Last modified time: 2017-05-22T19:57:14+08:00
# @Copyright: The full copyright is belong to Bingo Wan
import re
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
def getdata():
    with open('result') as files:
        f = files.readlines()
        datalist = []
        for data in f:
            d = re.split(':', data)[-1].strip('%<br>\n')
            datalist.append(float(d))
        return datalist
data = getdata()
sd = stanDeviation(data)
print sd
