# -*- coding: utf-8 -*-
"""
Preparing for an Exam

Created:  2022-03-01
Last modified: 2022-03-02

@author: Tanner Kirk

#Outside Help
https://www.geeksforgeeks.org/python-get-the-index-of-first-element-greater-than-k/
For printing first index with a value greater than defined value

"""

# =============================================================================
# This script will determine how many questions must be studied on a X number 
# of questions exam that consists of questions from test bank of n questions 
# in order to ensure that you will have a 90% and 95% chance to recognize at 
# least Y number of the questions. 
# 
# The number of questions in the test bank, number of questions on the exam, 
# and the number you wish to be familiar with can all be edited using the 
# appropriate variable
# =============================================================================


import numpy as np
import more_itertools

#Generate Random Seed
rng = np.random.default_rng()

#Number of Questions from Bank that will be on Exam
onExam = 10

#Number of questions in test bank
testBank = 42

#How many familar
familiar = 6

#Create an Array of numbers 1-42
questions = np.linspace(1,testBank,testBank)



#Define Positional Arguments
args = (questions, onExam, False)

#Define an array for tracking percentages
percentages = np.zeros((testBank,1))


#Loop represents number studied, will investigate likeihood at each number
#Of questions studied
for i in range(testBank):
    
    
    #Generate a list of length i that will represent questions studied
    #Convert to a set so it can be used in .intersections
    listStudied = np.linspace(1,i,i)
    listStudied = set(listStudied)
    
    #Generate possible exams
    possibleExams = more_itertools.repeatfunc(rng.choice, 10000, *args)
    
    
    #Set track variables to zero prior to loop
    (numExams, numFam) = (0,0)
    
    #Loop for through possible exams generated
    for exam in possibleExams:
        
        #Track number of exams stepped through
        numExams += 1
        
        #Find the number of studied questionst that are in the exam being 
        #investigated
        L = len(listStudied.intersection(set(exam)))
        
        #If number familiar or more intersection increase indexer
        if L >= familiar:
            numFam += 1
    
    #Calculate the percentage and store
    percentages[i] = numFam/numExams


#Print number of questions that need to be studied to be x% confident
res = next(x for x, val in enumerate(percentages)
                                  if val > 0.9) 

print ("To be 90% confident study " + str(res+1) + " questions.")

res = next(x for x, val in enumerate(percentages)
                                  if val > 0.95) 

print ("T0 be 95% confident study " + str(res+1) + " questions.")  
