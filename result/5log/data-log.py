
# coding: utf-8

# In[34]:

import re
def data_hz():
    with open('./hz_log_raw') as files:
        f = files.readlines()
        dataset = []
        for data in f:
            dataset.append(float(re.split(' ', data)[-1].strip('\n')))
        fw = open('./hz1.dat','w')
        for i in range(7):
            fw.write('%s   %10s\n'% (dataset[i], dataset[i+7]))   
        fw.close()
data_hz()

def data_sq():
    with open('./sq_log_raw') as files:
        f = files.readlines()
        dataset = []
        for data in f:
            dataset.append(float(re.split(' ', data)[-1].strip('\n')))
        fw = open('./sq1.dat','w')
        for i in range(7):
            fw.write('%s   %10s\n'% (dataset[i], dataset[i+7]))   
        fw.close()
data_sq()

def data_jx():
    with open('./jx_log_raw') as files:
        f = files.readlines()
        dataset = []
        fw = open('./jx2.dat', 'w')
        for data in f:
            usage = re.split('Used=|Used%=', data)[1].strip(' ')
            used = re.split('Used=|Used%=', data)[2].strip('%|\n')
            fw.write('%s  %10s\n'%(usage, used))        
data_jx()


# In[ ]:



