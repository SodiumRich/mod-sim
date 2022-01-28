# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:15:55 2022

@author: kirkt
"""

import numpy as np
import random
import matplotlib.pyplot as plt

#Define number of runs
runs = 10000

#Define Yes Counter and Accept None Arrays to track if best applicant or no applicants were accepted
yescounter = np.zeros((runs,30))
accept_none = np.zeros((runs,30))


#i tracks loops through numbmer of runs
for i in range(runs):
    #Fills applicants with a random sample with no replicates ranging from 1 to 30
    applicants = random.sample(range(0,30),30)

    #m tracks loops through each look phase
    for m in range(30):
        
        #if there is no look phase, the first applicant is only accepted if it is the best applicant
        if m == 0:
            
            #increase yescounter for the ith row and the mth column if the first applicant is the best
            if applicants[0] == 0:
                yescounter[i][m] = 1
            
            #make sure the yescounter in the ith row and mth column is zero if first applicant is not accepted
            else:
                yescounter[i][m] = 0
        
        
        #if it is not the first look phase move on to this set of logic
        else:
            
            #Find the minimum value in the look phase
            best_look = min(applicants[:m])
            
            #If the best applicant was found in the look phase then no one will be accepted as no one in the leap phase will be better
            if best_look == 0:
                
                #indicates the location of the best applicant in the look phase
                accept_none[i][m] = 1
            
            #if the best applicant is not found in the look phase continue to this logic
            #k will step through all applicants after the look phase
            for k in applicants[m:]:
                
                #if the value in applicants is better than the best look continue
                if k < best_look:
                    
                    #only interested in finding probability of finding best applicant, so if k is best applicant record a success
                    if k == 0:
                        yescounter[i][m] = 1
                        
                    #otherwise it is a failure and record this to make sure it is tracked correctly   
                    else:
                       yescounter[i][m] = 0
                

#Sum down the columns of each array
yescountersum = yescounter.sum(axis=0)
accept_none_sum = accept_none.sum(axis=0)

#Divide the new sum arrays by runs
probability = yescountersum/runs
probability_none = accept_none_sum/runs


#Plotting
fig, axs = plt.subplots(2, 1, constrained_layout=True)
axs[0].plot(np.linspace(0, 30, 30) , probability)
axs[0].set_title('Probability of Finding Best Applicant')
axs[0].set_xlabel('Number in Look Phase')
axs[0].set_ylabel('Probability')


axs[1].plot(np.linspace(0, 30, 30) , probability_none)
axs[1].set_title('Probability of Accepting None')
axs[1].set_xlabel('Number in Look Phase')
axs[1].set_ylabel('Probability')

