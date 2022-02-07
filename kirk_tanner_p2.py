# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 10:43:59 2022

@author: kirkt
"""

import time
import numpy as np
import matplotlib.pyplot as plt

def p2 (size = None, method = 'NR', seed = None, returnSeed = False):
   
    # =============================================================================
    # # =============================================================================
    # #     Produce an arry of random numbers
    # #     
    # #     Parameters
    # #     
    # #     size : define shape of output
    # #         type: int or tuple of ints
    # #     
    # #     method : algorithm to use
    # #         type: string
    # #             
    # #     seed : allow for input of manual seed
    # #         type: float
    # #     
    # #     returnSeed : if true, return seed
    # #         type: boolean
    # #     
    # #     Who Helped Me: Jodie Lawson (helped me better understand the creating of the array for the tuple case)
    # # =============================================================================
    # =============================================================================

    
    if method == 'NR':
        a = 1664525
        b = 1013904223
        c = 2**32
        
    elif method == 'RANDU':
        a = 65539
        b = 0
        c = 2**31
        
    else:
        raise Exception('Error - no such method')
     
    seed = ((time.time() % 1) * 1e12) % c   
    
    #Size determines array size, dtermine if int, tuple, or none
    if type(size) is int:
        
        y = np.zeros(size)
        y[0] = seed
        
        for i in range(1, size):
            y[i] = (a * y[i-1] + b) %c

    if size==None:
        y = seed
        
    if type(size) is tuple:
        
        y = np.zeros((size[0],size[1]))
        
        
        for i in range(0, size[0]):
            
            if i == 0:
                y[0][0] = seed
            
            else:
                y[i][0] = (a * y[i-1][-1] + b) %c
            
            for m in range(1, size[1]):
                
                y[i][m] = (a * y[i][m-1] + b) %c
                
    
    if returnSeed == False:
        return y/c
    
    else:
        return y/c, seed


# =============================================================================
# 
# NR = p2((5000,3))
# RANDU = p2((5000,3),'RANDU')          
# Python = np.random.random_sample((5000,3))
# 
# 
# 
# plt.figure(1)
# axis = plt.axes(projection = '3d')
# axis.scatter3D(RANDU[:,0],RANDU[:,1],RANDU[:,2], s = 1)
# plt.title('RANDU')
# axis.view_init(elev=32,azim=-127)
# 
# plt.figure(2)
# axis = plt.axes(projection = '3d')
# axis.scatter3D(NR[:,0],NR[:,1],NR[:,2], s = 1)
# plt.title('NR')
# axis.view_init(elev=32,azim=-127)
# 
# plt.figure(3)
# axis = plt.axes(projection = '3d')
# axis.scatter3D(Python[:,0],Python[:,1],Python[:,2], s = 1)
# plt.title('Numpy Random')
# axis.view_init(elev=32,azim=-127)  
# =============================================================================


# =============================================================================
# seed = np.zeros((5000,3))
# for i in range(5000):
#     for m in range(3):
#         seed[i][m] = ((time.time() % 1) * 1e12) % 2**32   
# 
# 
# plt.figure(1)
# axis = plt.axes(projection = '3d')
# axis.scatter3D(seed[:,0],seed[:,1],seed[:,2], s = 1)
# plt.title('RANDU')
# 
# =============================================================================

