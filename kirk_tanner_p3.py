# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 17:58:40 2022
Homework P3
Tanner Kirk


Outside Help:
    Jodie Lawson: Setting the Correct Jacobian
    StackOverflow: Setting axis' to be equal in size
    https://stackoverflow.com/questions/17990845/how-to-equalize-the-scales-of-x-axis-and-y-axis-in-matplotlib
                    
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from timeit import default_timer as timer

def pendulum(thetaZero = 30., damp = 0., timeSpan = 20., length = 0.45,\
             gravity = 9.80, wZero = 0.): 
    """
    Parameters
    ----------
    thetaZero : TYPE: float
        DESCRIPTION: Initial displacement angle (degrees)
        
    damp : TYPE: float
        DESCRIPTION: Damping coefficient 
        
    timeSpan : TYPE: float
        DESCRIPTION: Time length for simulation 
        
    length : TYPE: float
        DESCRIPTION: Length of pendulum 
        
    gravity : TYPE: float
        DESCRIPTION. Acceleration due to gravity 
        
    wZero : TYPE: float
        DESCRIPTION: Initial  angular  velocity  (degrees/s)\
            (positive for counterclockwise) 

    Returns
    -------
    None.
    
    Function creates an animation that compares two pendulums, one using simple
    harmonic motion and the other using differential equations and numerical
    methods

    """
    
    #Ensure these values are positive
    if damp < 0:
        raise ValueError('Error - damp cannot be negative')
        
    elif timeSpan < 0:
        raise ValueError('Error - timeSpan cannot be negative')
        
    elif length < 0:
        raise ValueError('Error - length cannot be negative')
        
    elif gravity < 0:
        raise ValueError('Error - gravity cannot be negative')
        
    
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
    diffX = np.zeros(len(t))
    diffY = np.zeros(len(t))
    
    #Use the Simple Model to find Theta and respective X and Y values
    for i in range(len(t)):
        thetaSimple[i] = thetaZeroRad * np.cos((np.sqrt(gravity/length))*t[i])
        simpleX[i] = length * np.sin(thetaSimple[i])
        simpleY[i] = length * np.cos(thetaSimple[i])
        
    
    #Define Differential Y[0] = theta, Y[1] = Angular Momentum
    def differential(t, y):
        dy = (y[1],
              -damp * y[1] - ((gravity * np.sin(y[0]))/length))
        return dy
    
    
    #Define Jacobian
    def jacob(t, y):
        jacobian = np.array([[0,1],
                             [ ((-gravity/length) * np.cos(y[0])),-damp]])
        return jacobian
    
    
    #Solve Differentials
    sol = integrate.solve_ivp(fun = differential,
                              t_span = [np.min(t), np.max(t)], 
                              y0 = [thetaZeroRad, wZeroRad],
                              t_eval = t, method = "Radau", jac = jacob)
    
    
    #Use Solution to Find X and Y values
    for i in range(len(t)):
        diffX = length * np.sin(sol.y[0])
        diffY = length * np.cos(sol.y[0])
    
    
    #Define Plot Details
    plt.cla()
    diff, = plt.plot([], [], 'ob-', label = "Actual Pendulum")
    simple, = plt.plot([], [], 'or--', label = "Simple Oscillator")
    plt.legend()
    plt.title("Simle Harmonic Oscillator vs An Actual Pendulum")
    plt.xlabel("X Coordinate (m)")
    plt.ylabel("Y Coordinate (m)")
    
    #Limit Axis Size so Pendulum is Centered
    plt.xlim([-length-0.25,length+0.25])
    plt.ylim([-length-0.25 ,length + 0.25])
    
    #This scales the axis to be the same size on the screen. 
    #Prevents the pendulum from seemingly increasing in size
    plt.gca().set_aspect('equal', adjustable='box') 
    
    
    #Plot the bottom point on the pendulum, as well as a point at (0,0) 
    #and a Line Between the Points for each model 
    for xPoint, yPoint, diffXPoint, diffYPoint \
        in zip(simpleX, simpleY, diffX, diffY):
            simple.set_data([0,xPoint],[0,-yPoint])
            diff.set_data([0,diffXPoint],[0,-diffYPoint])
            plt.pause(runTimeStep)
        
    
    return

pendulum(wZero = 100000000)