# -*- coding: utf-8 -*-
"""
Big Trouble on Little Elba: A discrete-variable stochastic model

Created:  2016-09-28
Last modified: 2021-02-19

@author: jrathman, Tanner Kirk
"""

import numpy as np
import matplotlib.pyplot as plt

def elba(n0 = (20999, 10000, 1, 0), R = (0.20, 0.20, 0.10, 0.10), \
         timeSpan = 120, nMax = 2000000, nRun = 1):
    """
    The small isolated island of Elba has a population of 32,000 people. Drawing 
    on our knowledge of chemical kinetics and reactor design, we propose a network 
    of elementary “reactions” to model how a contagious disease will spread in the
    population of hapless residents of Elba.
    
    Parameters:
        
        n0: Type: Tuple of ints 
            DESCRIPTION: Initial Numbers (healthy willing to be vaccinated, 
            healthy not willing to be vaccinated, sick people, vaccine doses)
            (the first three integers should sum to 32,000)
            
        R: Type: Tuple 
            DESCRIPTION: Rate constant adjustment factors (R5, R6, R7, R8)
            
        timeSpan: Type: Float
            DESCRIPTION: Length of simulation (days)
            
        nMax: Type: Int
            DESCRIPTION: Maximum allowed number of reactions for Gillespie algorithm
            
        nRun: Type: Int
            DESCRIPTION: Number of times to run the simulations, must be >= 1
                         if greater than 1 a histogram showing total death tolls
                         will be generated instead
        
    Returns:
        None
    """
    #Error Raising
    if nRun < 1:
        raise ValueError('Number of runs must be greater than or equal to 1')
    if timeSpan <= 0:
        raise ValueError('Time span must be greater than 0')
    
    
    #Redefine n0 to contain the other values such as IN, IV, SIN, SIV, D
    #Want in this order
    #H, F, S, IN, IV, SIN, SIV, D, V
    n0 = list(n0)
    for i in range(5):
        n0.insert(3, 0)
    n0 = tuple(n0)

    
    #Set rate constants (units 1/day)
    k1, k2, k3, k4, k5, k6, k7, k8 = (1.76e-5, 0.100, 0.01, 3.52e-6,\
                                      R[0] * 1.76e-5, R[1] * 1.76e-5,\
                                      R[2] * 0.010, R[3] * 0.010) 
    
    #Tuple of rate constants (1/day)
    k = (k1, k2, k3, k4, k5, k6, k7, k8)
    
    
    #For case where only one run is performed
    if nRun == 1:
        
        #Call Gillespie
        gills, nReactions, reactionRecord = gillespie(n0, timeSpan, k, nMax)
        t = gills[0]
        n = gills[1]


        #Pull or Solve for values needed in plots
        #Final Death Counter
        nDead = n[-1, 7]
        
        #Number of Healthy Individuals H + F
        nHealthy = np.sum(n[:,0:2], axis = 1)

        #Number of Sick Individuals S + SIN + SIV
        nSick = np.sum(n[:,(2,5,6)], axis = 1)
        
        #Number of Immune Individuals IN + IV
        nImmune = np.sum(n[:, (3,4)], axis = 1)
        
        #Preallocate Tracking Terms Second and Third Plots
        vacSick= np.zeros((len(t), 1))
        nonVacSick = np.zeros((len(t), 1))
        sDied = np.zeros((len(t), 1))
        sinDied = np.zeros((len(t), 1))
        sivDied = np.zeros((len(t), 1))
        
        #Determine when which reaction occurs
        for i in range(len(t)):
            
            #Casees where vaccinated person gets sick
            if reactionRecord[i] >= 12 and reactionRecord[i] <= 14:
                vacSick[i] = 1
                
            #Cases where nonvaccinated persons get sick
            elif (reactionRecord[i] >= 0 and reactionRecord[i] <= 5)\
                or (reactionRecord[i]>= 9 and reactionRecord[i] <= 11 ):
                nonVacSick[i] = 1
                
            #Cases where sick invdiviual Dies
            elif reactionRecord[i] == 7:
                sDied[i] = 1
                
            #Cases where naturally immune individual dies
            elif reactionRecord[i] == 17:
                sinDied[i] = 1
                
            #Cases where vaccinated individual Dies
            elif reactionRecord[i] == 18:
                sivDied[i] = 1
                
        #Cumulative Sums of above cases
        cumVacSick = np.cumsum(vacSick)
        cumNonVacSick = np.cumsum(nonVacSick)
        cumSDied = np.cumsum(sDied)
        cumSinDied = np.cumsum(sinDied)
        cumSivDied = np.cumsum(sivDied)
        
        
        #Plotting
        #Set Up Sub Plots
        fig, (ax0, ax1, ax2) = plt.subplots(nrows = 1, ncols = 3, \
                                            constrained_layout=True)
        
        #Main Title
        fig.suptitle('Stochastic Model of Elba Epidemic\nn0 = ' + str(n0) + \
                     ', nReactions = ' + str(int(nReactions)))    
        
        
        #Define First Subplot: Healthy, Sick, Immune, Dead vs Time
        #Plot Data
        ax0.plot(t, nHealthy, label='Healthy')
        ax0.plot(t, nSick, label='Sick')
        ax0.plot(t, nImmune, label='Immune')
        ax0.plot(t, n[:,7], label='Dead')
        
        #Set Limits
        ax0.set_xlim(0, timeSpan)
        ax0.set_ylim(-500, 35000)
        
        #Set Labels
        ax0.set_title('Elba vacation for Gillespie: nReactions = ' +\
                  str(int(nReactions)))
        ax0.set_xlabel('Time (Days)')
        ax0.set_ylabel('Number of People')
        ax0.text(timeSpan-30, nDead+500, 'Death Toll = ' + str(int(nDead)))  
        ax0.legend()
        
        
        #Define Second Subplot: Cumulative vac vs nonvac rates
        #Plot Data
        ax1.plot(t, cumVacSick, label='Vaccinated')
        ax1.plot(t, cumNonVacSick, label='Nonvaccinated')
        
        #Set Limits
        ax1.set_xlim(0, timeSpan)
        ax1.set_ylim(-500, np.max(cumNonVacSick)+5000)
        
        #Set Labels
        ax1.set_title('Cases Vaccinated vs. Nonvaccinated')
        ax1.set_xlabel('Time (Days)')
        ax1.set_ylabel('Number of Cases')


        #Define Third Subplot: Deaths from each Group
        #Plot Data
        ax2.plot(t, cumSDied, label='No Immunity')
        ax2.plot(t, cumSinDied, label='Natural Immunity')
        ax2.plot(t, cumSivDied, label='Vaccinated')
        
        #Set Limits
        ax2.set_xlim(0, timeSpan)
        ax2.set_ylim(-5, np.max(cumSDied)+500)
        
        #Set Labels
        ax2.set_title('Deaths by Group')
        ax2.set_xlabel('Time (Days)')
        ax2.set_ylabel('Number of People')

    
    #When number of runs is greater than 1
    else:
        #Preallocate array for tracking deaths
        deathArray = np.zeros(nRun)
        
        #Run Gillespie algorithm nRun times
        for i in range(nRun):
            
            #Call Gillespie
            gills, nReactions, reactionRecord = \
                gillespie(n0, timeSpan, k, nMax)
            
            #Store Death Counters
            n = gills[1]
            deathArray[i] = n[-1, 7]
        
        #Convert from Floats to Ints for use in plt.hist
        deathArrayInt = deathArray.astype(int)
        
        #Define Histogram bin width
        binWidth = 100
        
        #Histogram Plot
        #Plot Data
        plt.hist(deathArrayInt, bins = range(min(deathArrayInt), \
                                             max(deathArrayInt) \
                                            + binWidth, binWidth))
        
        #Set Labels
        plt.title('Histogram of Death Toll (' + str(int(nRun)) + \
                  ' Simulations)')
        plt.xlabel('Number of Deaths')
        plt.ylabel('Frequency')

    return



def gillespie(n0, timeSpan, k, nMax):
    """
    Gillespie algorithm implemented for epidemic on Elba.
    
    Parameters:
        n0: initial values of dependent variables
        timeSpan: duration of simulation
        k: reaction rate constants (1/day)
        nMax: maximum allowed number of reactions (time steps)
    
    Returns:
        (t, n): tuple of 1D array of time (t) and 2D array n
        nReactions: number of reactions (time steps)
    """
    
    #Unpack Rate Constants
    k1, k2, k3, k4, k5, k6, k7, k8  = k

    """
    Reaction network has 19 reactions and we have 9 species, so we need a
    19 x 9 matrix of stoiciometric cofficients. Column order must be the same
    as used in n0: H, F, S, IN, IV, SIN, SIV, D, V 
    """
    #Reaction Network with reactions and reaction number commented
    v = np.array([[-1, 0, 1, 0, 0, 0, 0, 0, 0],  # H + S -> 2S              0
                  [-1, 0, 1, 0, 0, 0, 0, 0, 0],  # H + SIN -> S + SIN       1
                  [-1, 0, 1, 0, 0, 0, 0, 0, 0],  # H + SIV -> S + SIV       2
                  [0, -1, 1, 0, 0, 0, 0, 0, 0],  # F + S -> 2S              3
                  [0, -1, 1, 0, 0, 0, 0, 0, 0],  # F + SIN -> S + SIN       4
                  [0, -1, 1, 0, 0, 0, 0, 0, 0],  # F + SIV -> S + SIV       5
                  [0, 0, -1, 1, 0, 0, 0, 0, 0],  # S -> I                   6
                  [0, 0, -1, 0, 0, 0, 0, 1, 0],  # S -> D                   7
                  [-1, 0, 0, 0, 1, 0, 0, 0, -1], # H + V -> IV              8
                  [0, 0, 0, -1, 0, 1, 0, 0, 0],  # IN + S -> SIN + S        9
                  [0, 0, 0, -1, 0, 1, 0, 0, 0],  # IN + SIN -> 2SIN         10
                  [0, 0, 0, -1, 0, 1, 0, 0, 0],  # IN + SIV -> SIN + SIV    11
                  [0, 0, 0, 0, -1, 0, 1, 0, 0],  # IV + S -> SIV + S        12
                  [0, 0, 0, 0, -1, 0, 1, 0, 0],  # IV + SIN -> SIV + SIN    13
                  [0, 0, 0, 0, -1, 0, 1, 0, 0],  # IV + SIV -> 2SIV         14
                  [0, 0, 0, 1, 0, -1, 0, 0, 0],  # SIN -> IN                15
                  [0, 0, 0, 0, 1, 0, -1, 0, 0],  # SIV -> IV                16
                  [0, 0, 0, 0, 0, -1, 0, 1, 0],  # SIN -> D                 17
                  [0, 0, 0, 0, 0, 0, -1, 1, 0]]) # SIV -> D                 18
    
    #Pre-allocate arrays for t, n and reaction record
    t = np.zeros((nMax, 1))
    n = np.zeros((nMax, 9))
    reactionRecord = np.zeros((nMax, 1))
    
    #Set first row (at time zero) of matrix n to n0
    n[0, :] = n0 
    
    #Initialize reaction counter
    nReactions = 0
    
    for i in range(1, nMax):
        H, F, S, IN, IV, SIN, SIV, D, V = n[i-1, :]
        
        #Calculate proportional reaction probabilities
        r = np.array([k1 * H * S,
                      k1 * H * SIN,
                      k1 * H * SIV,
                      k1 * F * S,
                      k1 * F * SIN,
                      k1 * F * SIV,
                      k2 * S,
                      k3 * S,
                      k4 * H * V,
                      k5 * IV * S,
                      k5 * IN * SIN,
                      k5 * IN * SIV,
                      k6 * IV * S,
                      k6 * IV * SIN,
                      k6 * IV * SIV,
                      k2 * SIN,
                      k2 * SIV,
                      k7 * SIN,
                      k8 * SIV])
        #Sum r
        rtot = np.sum(r)
        
        #Determine if reaction occurs
        if rtot == 0:
            break
        else:
            nReactions += 1
        
        #Uniform Random Number to Generate Time Interval
        w = np.random.uniform()
        
        #Compute Time Interval
        tau = -np.log(w) / rtot
        
        #Update Simulation Time
        t[i] = t[i-1] + tau
        
        #Calculate Reaction Probabilities
        p = r / rtot
        
        #Calculate Cumulative Sums
        csp = np.cumsum(p)
        
        #Uniform random Number to Select which Reaction Occurs
        q = np.random.uniform()
        
        #Determine which reaction will occur
        j = np.where(q < csp)[0][0]
        
        #Run that reaction and store in next row of n
        n[i, :] = n[i-1, :] + v[j, :]
        
        #Record which reaction occurs
        reactionRecord[i] = j
        
        #If timestep larger than max time span stop
        if t[i] >= timeSpan:
            break
    
    #Record data and will remove excess rows from t, n, and reactionRecord
    if nReactions < nMax:
        t = t[0:nReactions+1]
        n = n[0:nReactions+1, :]
        reactionRecord = reactionRecord[0:nReactions+1]
    
    return (t, n), nReactions, reactionRecord

#=============================================================================
#Self-test code
if __name__ == '__main__':
    deathArray = elba(n0 = (20999, 10000, 1, 1400), timeSpan = 120, nRun = 40)