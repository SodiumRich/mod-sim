# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 17:58:40 2022

@author: kirkt
"""
import numpy as np
import matplotlib.pyplot as plt

def pendulum(thetaZero = 30, damp = 0, timeSpan = 5, length = 1,\
             gravity = 9.80, wZero = 0): 
    """
    Parameters
    ----------
    thetaZero : TYPE, float
        DESCRIPTION. Initial displacement angle (degrees)
    damp : TYPE, float
        DESCRIPTION. Damping coefficient 
    timeSpan : TYPE, float
        DESCRIPTION. Time length for simulation 
    length : TYPE, float
        DESCRIPTION. Length of pendulum 
    gravity : TYPE, float
        DESCRIPTION. Acceleration due to gravity 
    wZero : TYPE, float
        DESCRIPTION. Initial  angular  velocity  (degrees/s)\
            (positive for counterclockwise) 

    Returns
    -------
    None.

    """
    
    #Ensure these values are positive
    if damp < 0:
        raise Exception('Error - damp cannot be negative')
        
    if timeSpan < 0:
        raise Exception('Error - timeSpan cannot be negative')
        
    if length < 0:
        raise Exception('Error - length cannot be negative')
        
    if gravity < 0:
        raise Exception('Error - gravity cannot be negative')
        
    
    #Convert Degrees to Radians
    thetaZeroRad = thetaZero * np.pi / 180
    wZeroRad = wZero * np.pi / 180
    
    #Generate a Time Step based on Refresh Rate of Monitor
    refreshRate = 144
    runTimeStep = 1/refreshRate
    realTimeStep = runTimeStep
    t = np.arange(0, timeSpan, realTimeStep)
    
    #Define Arrays Based off Time Length
    thetaSimple = np.zeros(len(t))
    simpleX = np.zeros(len(t))
    simpleY = np.zeros(len(t))
    
    
    #Use the Simple Model to find Theta and respective X and Y values
    for i in range(len(t)):
        thetaSimple[i] = thetaZeroRad * np.cos((np.sqrt(gravity/length))*t[i])
        simpleX[i] = length * np.sin(thetaSimple[i])
        simpleY[i] = length * np.cos(thetaSimple[i])
        
        
    #Define Plot Details for Simple Plot
    plt.cla()
    simple, = plt.plot([], [], 'o--')
    plt.xlim([-length-0.25,length+0.25])
    plt.ylim([-length-0.25 ,0.25])
    
    for xPoint, yPoint in zip(simpleX, simpleY):
        simple.set_data([0,xPoint],[0,-yPoint])
        plt.pause(runTimeStep)
        
        
    return thetaSimple, simpleX, simpleY


thetaSimple, simpleX, simpleY = pendulum()