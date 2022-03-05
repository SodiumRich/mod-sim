# -*- coding: utf-8 -*-
"""
Spyder Editor

Created: Long ago, far away
Last modifed: 2022-03-04

@authors: jim.rathman,Tanner Kirk, Herr Hoffman

Jim Rathman: Initial Seqscore_target, and seekuence Functions
Herr Hoffman: Initial levenshtein function
Tanner Kirk: Commenting, and edits needed to make all functions work together


"""

import string
import random
import numpy as np

#String of allowed characters
char = string.ascii_letters + string.digits + string.punctuation + ' '
target = "Half man, half bear, half pig - it's ManBearPig!"

def seqscore_target(inseq=None, target = None):
    """
    Calculates and returns the similarity score between a query string and the
    target string.
    
    Parameters:
        inseq: Type: str
            Sequence to be compared to target sequence
        target: Type: str
            Target sequence
        
    Returns:
        score: Type: int
            Number of matched characters in correct position in sequence.
            
        match: Type: boolean
            True if the query sequence is the same as the target sequence.
    """
    #Error handling
    if type(inseq) is not str:
        raise TypeError('Query sequence must be a string')

    
    #Lengths of query string and target string
    lenTarget = len(target)
    lenQuery = len(inseq)
    
    #Initialize score
    score = 0 
    
    #If query and target have same character in same position increment score
    for a, b in zip(inseq, target):
        if a == b:
            score += 1
    
    #If the query and target are the same length, and the score is equal to the 
    #length of the target, the two are the same. Return true
    if score == lenTarget and lenQuery == lenTarget:
        match = True
    else:
        match = False
    
    return score, match

#==============================================================================

def levenshtein(seq1, seq2):
    """
    Determines the distance of query string from the target string
    Distance being the number of change needed to make one string into the other
    
    Parameters:
        seq1: Type: str
            sequence 1
        
        seq2: Type: str
            sequence 2
            
    Returns:
        matrix[size_x - 1, size_y - 1]: Type: Int
            The value that represents the number of changes for the two strings
            to be equivalent
    """
    #Determine array size necessary for levenshtein algorithm
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    
    #Initialize Matrix 
    matrix = np.zeros ((size_x, size_y))
    
    #Insert Integers increasing by one across first row of matrix
    for x in range(size_x):
        matrix [x, 0] = x
    
    #Insert integers increasing by on down the first column of the matrix
    for y in range(size_y):
        matrix [0, y] = y

    #Loop through array row wise and column wise
    for x in range(1, size_x):
        for y in range(1, size_y):
            
            #If the two values are equal
            if seq1[x-1] == seq2[y-1]:
                
                #Set the matrix at x,y to be the min of these values
                #This shows that no extra change is needed
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
                
                #Set the matrix at x,y to be the min of these values
                #This will show that a change is needed
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )

    
    #Return the number of changes required for seq 1 and seq 2 to be the same
    return (matrix[size_x - 1, size_y - 1])



#==============================================================================

def seekuence(length, nChildren=20, mutationProbs=(0.01, 0.002, 0.001),\
              scoringFun = 'seqscore_target'):
    """
    Applies an evolutionary algorithm to alter a string of characters, and
    determine the best "child" string in that generation.
    
    Parameters:
        length: Type: int
            Define length of query sequence
            
        nChildren: Type: int
            Number of "children" in each generation
            
        mutationProbs: Type: float
            Alter probabilites for substitution, deletion, and insertion
            respectively
        
    Returns:
        None
    """
    
    #Unpack probablities
    subProb, delProb, insProb = mutationProbs  
    
    #Initialize Generation Counter
    generation = 0
    
    #Intialize Match
    match = False
    
    #Generate a random query string of length determined by input
    parent = ''.join(random.choice(char) for x in range(length))
    
    #Loop until query string is target string
    while not match:
        
        #Initialize score        
        score = None
        
        #Generate number of children for generation
        for i in range(nChildren):
            #initialize child string
            child = ''
            
            #Loop through parent string and determine subs, dels, insertions
            #Based on mutation probability
            for a in parent:
                
                #Allow for one possible mutation per site
                mutation = random.choice(('sub', 'del', 'ins'))
                
                #If mutation is sub and its probabiltiy is met, 
                #sub character in position a
                if mutation == 'sub' and np.random.binomial(1, subProb) == 1:
                    a = random.choice(char)
                    
                #If mutation is del and its probabiltiy is met, 
                #del character in position a
                elif mutation == 'del' and np.random.binomial(1, delProb) == 1:
                    a = ''
                    
                #If mutation is ins and its probabiltiy is met, 
                #ins character in position a
                elif mutation == 'ins' and np.random.binomial(1, insProb) == 1:
                    
                    #Determine if insertion occurs before or after a
                    side = random.choice(('before', 'afer'))
                    
                    #Place Before
                    if side == 'before':
                        a = random.choice(char) + a
                        
                    #Place After
                    else:
                        a = a + random.choice(char)
                
                #Perform insertion        
                child = child + a
            
            #Select scoring function
            if scoringFun == 'seqscore_target':
            
                #Determine Score of this child
                tem, match = seqscore_target(child,target)
    
                #If there is no current score, or the new childs score is greater
                #than the current best, or the child is the target sequence
                if score is None or tem > score or match:
                    
                    #Set the score for this child as the new highest score
                    score = tem
                    
                    #Set the new best child as the parent for the next generation
                    next_parent = child
                
                if match:
                    break
            
            elif scoringFun == 'levenshtein':
                
                #Determine Score of this Child
                distance = levenshtein(child, target)
                
                if score is None or distance < score or distance == 0:
                    
                    #Set the score for this child as the new highest score
                    score = distance
                    
                    #Set the new best child as the parent for the next generation
                    next_parent = child
                
                if distance == 0:
                    break
                
            else:
                raise ValueError('Score Function must be levenshtein or\
                                 seqscore_target')
        
        #Set parent to best child from most recent generation
        parent = next_parent
        
        #Increment Generation
        generation += 1
        
        #Print the generation number, its current score, and the current parent
        print('Gen ', generation, '\tScore = ', score, '\t', parent)

#=============================================================================
#Self-test code #seqscore_target #levenshtein
if __name__ == '__main__':
    seekuence(48, 20, (0.01, 0.002, 0.001), 'levenshtein')