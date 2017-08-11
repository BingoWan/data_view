#! /usr/bin/env python 
# coding: utf-8

# In[1]:

import re
def data_joblog(s):
    with open('./%s_raw'%s) as files:
        f = files.readlines()
        dataset = []
        for data in f:
            d = re.split(':|,', data)[1].strip('T| \n')
            dataset.append(float(d))
        fw = open('./%s1.dat'%s, 'w')
        for i in range(7):
            print (dataset[6-i], int(dataset[13-i]))
            fw.write('%s   %d\n'%(dataset[6-i], int(dataset[13-i])))
namelist = ['hz', 'jx']
for name in namelist:
    data_joblog(name)
            


# In[ ]:



