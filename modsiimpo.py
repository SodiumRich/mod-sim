# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:15:55 2022

@author: kirkt
"""

import numpy as np
import random

#Define number of runs
runs = 10000
yescounter = np.zeros((runs,30))


for i in range(runs):
    applicants = random.sample(range(0,30),30) #Fills applicants with a random sample with no replicates ranging from 1 to 30
    
    for m in range(30):
        
        if m == 0:
            if applicants[0] == 0:
                yescounter[i][m] = 1
            else:
                yescounter[i][m] = 0
        
        else:
            best_look = min(applicants[:m])
            
            for k in applicants[m:]:
                if k < best_look:
                    if k == 0:
                        yescounter[i][m] = 1
                    else:
                       yescounter[i][m] = 0
                

yescountersum = yescounter.sum(axis=0)


print(yescountersum)


#Search range i runs
#Shuffle
#For m is zero take first value
#if m is not zero take the min(applicants[:m])
#for j in applicants[m:]: find the first valye less than x place in rank[i,m]
#break
