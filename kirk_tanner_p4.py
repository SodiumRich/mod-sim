# -*- coding: utf-8 -*-
"""
Mysteries of e

Created:  2022-02-28
Last modified: 2022-02-28

@author: Tanner Kirk
"""
# =============================================================================
# This script will calculate the he average number of uniformly-distributed 
# random numbers between 0 and 1 that must be added to give a sum ≥ 1.
# The number of runs can be increased to increase accuracy. 
# =============================================================================

import numpy as np

#Define Number of Runs
runs = 1000000

#Initialize an array to track number of numbers added to get a value >= 1
numberAdded = np.zeros((runs,1))

#Run the test runs number of times
for i in range(runs):
    
    #Reset Counter Variable Between Runs    
    counter = 0
    
    #This loop responsible for generating random numbers and tracking number
    #Generated
    for j in range(runs):   
        
        #Generate a uniform random number [0,1]
        randomNum = np.random.uniform()
        
        #Add the random numbers generated during this run together
        counter += randomNum
        
        #See if counter is greater than or equal to 1
        if counter >= 1:
            
            #Store the number of values needed to make the value >= 1 in the
            #numberAdded array at index i
            numberAdded[i] = j+1
            
            #Break back to i loop
            break

#Find the average number of numbers needed to get a value >= 1
average = np.average(numberAdded)

#Print the average
print(average)