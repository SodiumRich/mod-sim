# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:15:55 2022

@author: kirkt
"""

import numpy as np
import random

#Define number of runs
runs = 10000
applicants = []
yescounter = [0] * 30

for i in range(runs):
    applicants = random.sample(range(1,31),30) #Fills applicants with a random sample with no replicates ranging from 1 to 30
   
    for m in range(30):
        if m == 0: #For m of 0 the yes counter increases if and only if the first applicant is the best applicant
            if applicants[0] == 1:
                yescounter[m] += yescounter[m]
        else:
            end_index = m + 1
            subset_list = applicants[0:(m+1)]
            if np.min(subset_list) != 1:
                best_location = applicants.index(1,m+1)
                yescounter[best_location] += yescounter[best_location]
               
           
   

#Use a for loop for zero
#if one is found increase yes counter

#use a for loop to check 0-m and save min value
#compare this to rest of values
#if one is found increase yes counter