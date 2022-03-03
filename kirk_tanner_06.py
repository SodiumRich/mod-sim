# -*- coding: utf-8 -*-
"""
Preparing for an Exam

Created:  2022-03-02
Last modified: 2022-03-02

@author: Tanner Kirk

Outside Help:
    Jodie lawson reminding me how syntax works and debugging
    Ikra Anwar broad logic
"""
# =============================================================================
# This script will answer the following question statement:
# The year is 1883 and the place is a nameless, lawless town in Montana. 
# Three cowboys named Smithers, Johnson and Flynn are having a heated argument 
# about nothing important and they foolishly decide to settle it with a 
# shooting contest. The rules of their contest are rather unusual. They will 
# initially draw lots to determine who goes first, second, and third. They will 
# then take their places at the corners of a large triangle drawn in the dirt. 
# It is agreed that they will fire single shots in turn and continue in the  
# same order until two of them have been shot – the last cowboy standing will  
# be the winner. At each turn the man who is firing may aim wherever he 
# pleases. All three cowboys know that Smithers is the most accurate shooter  
# and Flynn the least They don’t know the specifics, but we do: Smithers’ 
# accuracy is 90%, Johnson’s is 80%, and Flynn’s is a dismal 50%. Each cowboy  
# adopts the best strategy for himself when it’s his turn to shoot. For example, 
# when it’s Flynn’s turn, if Smithers and Johnson are both still standing, 
# Flynn’s best strategy is to shoot up in the air, intentionally not trying to 
# hit anyone. (Do you understand why?) Estimate each cowboy’s probability of 
# winning this stupid contest. Which of these losers has the best chance to be 
# the winner? 
# 
# This script is not easily modular and no input is required by the user. 
# =============================================================================


import numpy as np
import random

#Define number of runs
runs  = 10000

#Define Run Tracker
whoWon = np.zeros((runs,6))


#Function that determines if shot was succesful
def chance(percentage = 0.0):
    if random.random() <= percentage:
        return True
    else:
        return False

for l in range(runs):
    #Loop through each turn order
    orderCount = 0
    
    #Find all permutations of turn order
    posTurnOrders = np.array([[0.5,0.8,0.9],
                             [0.5,0.9,0.8],
                             [0.8,0.5,0.9],
                             [0.8,0.9,0.5],
                             [0.9,0.5,0.8],
                             [0.9,0.8,0.5]])
    
    for order in posTurnOrders:       
        
        #Loop until sum of order is less than 1 (Only possible when 1 is alive)
        while np.sum(order) > 1:
            
            #Loop through order consecutively
            for i in range(3):
                
                #If order[i] is the highest value then it will attempt to shoot 
                #the middle most value
                if order[i] == np.amax(order):
                    
                    #Determine Success
                    if chance(order[i]):
                        
                        #Set the median value to 0 if sucessful
                        #Now there is a new low and median value in order
                        a = np.where(order == np.median(order))
                        order[a] = 0.0
                        
                #If order[i] is the median value then it will attempt to shoot
                #the highest value
                elif order[i] == np.median(order):
                    
                    #Determine sucess
                    if chance(order[i]):
                        
                        #If successful set the max value to 0
                        #Now there is a new low, high, and median
                        a = np.where(order == np.amax(order))
                        order[a] = 0.0
        
        #Track position and number of the person who won
        whoWon[l][orderCount] = np.sum(order)
        
        #Column Tracker
        orderCount += 1

#Track how many times each person was the last man standing
smithersWon = np.count_nonzero(whoWon == 0.9)
johnsonWon = np.count_nonzero(whoWon == 0.8)
flynnWon = np.count_nonzero(whoWon == 0.5)

#Calculate the percent chance each person is the last man standing
smithersChance = round((smithersWon/(runs * 6) *100),3)
johnsonChance = round((johnsonWon/(runs * 6) *100),3) 
flynnChance = round((flynnWon/(runs * 6) *100),3)

#Print the percent chance each individual will be the last man standing
print('Smithers\' Chance to Win: ' + str(smithersChance))
print('Johnson\'s Chance to Win: ' + str(johnsonChance))
print('Flynn\'s Chance to Win: ' + str(flynnChance))