# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 10:43:59 2022

@author: kirkt
"""

import time
import random
import numpy as np

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
        
    t = int( time.time() * 1000.0 )
    
    
    
    y = np.zeros(size())
    y[0] = seed()
    

    return