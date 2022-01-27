# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:15:55 2022

@author: kirkt
"""

import numpy as np
import random

#Define number of runs
runs = 1
applicants = []
yescounter = np.zeros((runs,30))


for i in range(runs):
    applicants = random.sample(range(0,30),30) #Fills applicants with a random sample with no replicates ranging from 1 to 30
   
    for m in range(30):
        if m == 0: #For m of 0 the yes counter increases if and only if the first applicant is the best applicant
            if applicants[0] == 0:
                yescounter[i,m] = 1
        else:
            best_look = min(applicants[:m])
            for k in applicants[m:]:
                print(k)
                if applicants[k] < best_look:
                    yescounter[i,k] = 1
                    break
                    

yescountersum = yescounter.sum(axis=0)


print(yescountersum)


#Search range i runs
#Shuffle
#For m is zero take first value
#if m is not zero take the min(applicants[:m])
#for j in applicants[m:]: find the first valye less than x place in rank[i,m]
#break
