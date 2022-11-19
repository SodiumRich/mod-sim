# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:37:29 2022



@author: kirkt
"""

import numpy as np
import math
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker

def myfinal(redTroops = 50, blueTroops = 50, redStrength = 5, \
            blueStrength = 10, nDays = None, size = 50, grid = True):
    """
    Parameters
    ----------
    redTroops : TYPE: int, optional
        DESCRIPTION. Initial number of red Troops, must be at least 1 and 
        at most 10, must be less than grid size
        The default is 50.
        
    blueTroops : TYPE: int, optional
        DESCRIPTION. Initial number of blue Troops, must be at least 1 and at 
        most 10, must be less than grid size
        The default is 50.
        
    redstrength : TYPE: int, optional
        DESCRIPTION. Relative strength of red Troops
        The default is 5.
        
    bluestrength : TYPE: int, optional
        DESCRIPTION. Relative strength of blue Troops
        The default is 10.
        
    nDays : TYPE, optional
        DESCRIPTION. Max number of days to let simulation run
        The default is None.
        
    size : Type: int, optional
        DESCRIPTION. Grid size, must be an even integer
        The default is 10
        
    grid : TYPE: Boolean, optional
        DESCRIPTION. If true display grid
        If false do not display Grid
        The default is True.

    Returns
    -------
    None.

    This function simulates two armies of set strength marching towards each
    other and then fighting. If red wins they take over the area converting it
    to red. Blue does likewise. The simulation continues until the set number
    of days is reached or one side takes over the entire area.
    """
    #ERROR HANDLING
    if size < redTroops:
        raise ValueError('Number of troops must be less than grid size')
    
    if size < blueTroops:
        raise ValueError('Number of troops must be less than grid size')
    
    if type(redTroops) is not int:
        raise TypeError('Number of troops must be an int')
    
    if type(blueTroops) is not int:
        raise TypeError('Number of troops must be an int')
        
    if type(redStrength) is not int:
        raise TypeError('Strength of troops must be an int')
        
    if type(blueStrength) is not int:
        raise TypeError('Strength of troops must be an int')
        
    if type(nDays) is not int and nDays != None:
        raise TypeError('Number of days must be an int or None')
        
    if type(size) is not int:
        raise TypeError('Grid size must be an int')    
        
    if (size % 2) != 0:
        raise ValueError('Grid size must be even')   
        
    #Set max number of gens
    maxGen = nDays

    #initialize masks 
    mask = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
 
    #Initialize Grid Size
    N = size 
    
    #Calculate Strength Ratio Red/Blue
    redStrengthRatio = redStrength / (blueStrength + redStrength)
    blueStrengthRatio = blueStrength / (blueStrength + redStrength)
                                      
    #Seed the Troops along left and right edges of battle field
    z = np.random.binomial(1, 0, (N, N))
    
    
    #Initialize Red Troops
    for i in range(redTroops):
        if i == 0:
            z[math.floor(size/2)][0] = 1
        if i > 0:
            if (i % 2) == 0:
                z[math.floor(size/2)+(i//2)][0] = 1
            else:
                z[math.floor(size/2)-math.ceil(i/2)][0] = 1

    #Initialize Blue Troops
    for i in range(blueTroops):
        if i == 0:
            z[math.floor(size/2)][size-1] = 2
        if i > 0:
            if (i % 2) == 0:
                z[math.floor(size/2)+(i//2)][size-1] = 2
            else:
                z[math.floor(size/2)-math.ceil(i/2)][size-1] = 2

    """
    The code below creates a color map with
        state 0 => position = 0.0   White (255, 255, 255) => (1, 1, 1)
        state 1 => position = 0.5  Red (0, 204, 0) => (0, 0.8, 0)
        state 2 => position = 1.00  Blue (255, 102, 0) => (1, 0.4, 0)
    """
    cdict = {'red':   ((0.00, 1.00, 1.00),
                       (0.5, 0.542, 0.542),
                       (1.00, 0.2539, 0.2539)),
             'green': ((0.00, 1.00, 1.00),
                       (0.50, 0.0, 0.0),
                       (1.00, 0.410, 0.410)),
             'blue':  ((0.00, 1.00, 1.00),
                       (0.50, 0.0, 0.0),
                       (1.00, 0.8789, 0.8789))}
    
    #Now create the colormap object
    colormap = colors.LinearSegmentedColormap('mycolors', cdict, 256)
    
    #Set up plot object    
    fig, ax = plt.subplots()
    plt.axis('scaled')
    plt.axis([0, N, 0, N])
    
    cplot = plt.pcolormesh(z, cmap = colormap, vmin = 0, vmax = 2)
    
    plt.title('Battle for Gridlandia - Day: '+ str(nDays))  
    
    #If grid is wanted add grid lines
    if grid:    
        plt.grid(True, which = 'both', color = '0.5', linestyle = '-')
        plt.minorticks_on()
        xminorLocator = ticker.MultipleLocator(1)
        yminorLocator = ticker.MultipleLocator(1)
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.yaxis.set_minor_locator(yminorLocator)

    #Initialize Stop Flag
    stopFlag = False
    
    #Set generation number to 1
    nDays = 1
    
    #Loop until a stop condition is met
    while not stopFlag:
        #Create an array that tells number of red next to each cell
        nWar_red = ndimage.generic_filter(z==1, np.sum, footprint = mask, 
                                       mode = 'constant', output = int)
        
        #Create an array that tells number of blue next to each cell
        nWar_blue = ndimage.generic_filter(z==2, np.sum, footprint = mask, 
                                       mode = 'constant', output = int)      
        #Rules rule!
        """
        States: unclaimed (0), red territory (1), blue territory (2)
        Rules:
          rule 1: If no enemy Troops march forward with a 25% chance of
                  moving succesfully

          rule 2: If enemy located in neighborhood fight dependent on strength
                  If red wins and blue loses red takes control of area
                  If blue wins and red loses blue takes control of area
                  If both win stalemate
                  If both lose stalemate
        """

        #Rule 1
        #Determine if Troop succesfully marches
        forwardMarch = np.random.binomial(1, 0.325, (N, N))
        
        #No Red Neighbors and next to Blue Neighbor and March success
        r1 = (z == 0) & (nWar_blue > 0) & (forwardMarch == 1)
        z[r1] = 2
        
        #No Blue Neighbors and next to Red Neighbor
        r1_2 = (z == 0) & (nWar_red > 0) & (forwardMarch == 1)
        z[r1_2] = 1


        #Rule 2        
        #Determine probabilities based on strengths and number of surrounding
        #enemies
        red_prob = (nWar_red * redStrengthRatio)/10
        blue_prob = (nWar_blue * blueStrengthRatio)/10
        
        #Determine if red won for each cell
        red_win = np.random.binomial(1, red_prob, (N, N))
        
        #Determine if blue won for each cell
        blue_win = np.random.binomial(1, blue_prob, (N, N))
        
        #Determine if both red and blue won the same cell
        #used to determine stalemate
        both_win = np.logical_and(red_win, blue_win)
        
        #Red Troop next to Blue Troop and Blue Wins, no stalemate
        r2_1 = (z == 1) & (nWar_blue > 0) & (blue_win == 1) & (both_win == 0)
         
        #Blue Troop Next to Red Troop Red Wins, No stalemate
        r2_2 = (z == 2) & (nWar_red > 0) & (red_win == 1) & (both_win == 0)
        
        #Set to blue
        z[r2_1] = 2
        
        #Set to red
        z[r2_2] = 1

        #Troop Counter
        redTotal = (z == 1).sum()
        blueTotal = (z == 2).sum()

        #Convert to 1D array
        cplot.set_array(z.ravel())
        plt.title('Battle for Gridlandia - Day: '+ str(nDays) +
                  '\nRed Troops:' + str(redTotal) +
                  '\nBlue Troops:' + str(blueTotal)) 
        
        #Pause so the change is more readable
        plt.pause(0.2)
        
        #Stop if max generation is reached
        if nDays == maxGen:
            stopFlag = True
        
        #Stop if no blue present
        if not (z == 2).any():
            plt.title('Battle for Gridlandia - Day: '+ str(nDays) + 
                      ' - Redinia WINS' + '\nRed Troops:' + str(redTotal)) 
            stopFlag = True
        
        #Stop if no red present
        if not (z == 1).any():
            plt.title('Battle for Gridlandia - Day: '+ str(nDays) + 
                      ' - Blueberg WINS' + '\nBlue Troops:' + str(blueTotal))
            stopFlag = True
        
        #Increase counter as next generation begins
        else:
            nDays += 1
            
    
#=============================================================================
#Self-test code
if __name__ == '__main__':
    myfinal()