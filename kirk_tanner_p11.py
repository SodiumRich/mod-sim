# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:21:24 2022

Cellular Automata: Forest fire

Created: 2016-11-16
Last revised: 2022-04-12
@author: jim.rathman and Tanner Kirk
"""

import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker

def bore(density = 0.6, neighborhood = 'vonNeumann', radius = 1, nGen = None, 
         pbc = False, grid = True):
    """
    Parameters
    ----------
    density : TYPE - Float, optional
        DESCRIPTION. Initial probability a site has a tree 
        The default is 0.6.
    
    neighborhood : TYPE - string, optional
        DESCRIPTION. 'vonNeumann' or 'Moore' defines the neighborhood type used
        vonNeumann - Results in a diamond shape up to radius r away from initial point
        Moore - Results in a square up to radius r away from initial point 
        The default is 'vonNeumann' contains.
    
    radius : TYPE - Int, optional
        DESCRIPTION. Radius of neighborhood must be 1 or 2
        The default is 1.
    
    nGen : TYPE - int, optional
        DESCRIPTION. Number of generations to run simulation for
        The default is None.
    
    pbc : TYPE - Boolean, optional
        DESCRIPTION. If true periodic boundary conditions (continous boundary)
        If false dead zone boundary conditions (hard boundary)
        The default is False.
    
    grid : TYPE - Boolean, optional
        DESCRIPTION. If true display gride
        If false do not display Grid
        The default is True.

    Raises
    ------
    ValueError
        DESCRIPTION.

    Returns
    -------
    None.

    """
    #Set max number of gens
    maxGen = nGen

    #At bit o' error handling    
    if neighborhood == 'Moore':
        if radius == 1:
            mask = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        elif radius == 2:
            mask = np.array([[1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 0, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],])
        else:
            raise ValueError('radius must be 1 or 2')
    elif neighborhood == 'vonNeumann':
        if radius == 1:
            mask = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        elif radius == 2:
            mask = np.array([[0, 0, 1, 0, 0],
                             [0, 1, 1, 1, 0],
                             [1, 1, 0, 1, 1],
                             [0, 1, 1, 1, 0],
                             [0, 0, 1, 0, 0],])
        else:
            raise ValueError('radius must be 1 or 2')
    else:
        raise ValueError("neighborhood must be 'Moore' or 'vonNeumann'")
    
    #Set the mode parameter for sp.ndimage.gaussian_filter() function
    if pbc:
        bc_mode = 'wrap' #periodic boundary conditions
    else:
        bc_mode = 'constant' #deadzone boundary conditions
 
    X = 70 #grid x size
     
    Y = 140 #grid y size
    
    #Seed the forest at specified density
    z = np.random.binomial(1, density, (X, Y))
    
    #Set 5x5 center to infected
    #Find healthy trees in center area
    k = z[33:38,68:73] == 1 

    #Set healthy trees in 5x5 center to infected
    for i in range(5):
        for j in range(5):
            if k[i][j]:
                z[33+i][68+j] = 2
        
    """
    Define colormap to use. Can pick from the many built-in colormaps, or,
    as shown below, create our own. First create a dictionary object with
    keys for red, green, blue. The value for each pair is a tuple of tuples.
    Must have at least 2 tuples per color, but can have as many as you wish. The
    first element in each tuple is the position on the colormap, ranging from
    0 (bottom) to 1 (top). For our CA, each position corresponds to one of the
    four possible states: 0 (bare ground), 1 (green tree) , 2 (burning tree),
    3 (burned-out stump).
    
    The second element is the brightness (gamma) of the color. The third element 
    is not used when we only have two tuples per color. The conventional red-green
    blue (RGB) color scale has gamma values ranging from 0 to 255 (256 total 
    levels); these are normalized 0 to 1. I.e., a gamma of 1 in the color tuple
    denotes gamma 255.
    
    The code below creates a color map with
        state 0 => position = 0.0   white (255, 255, 255) => (1, 1, 1)
        state 1 => position = 0.5  green (0, 204, 0) => (0, 0.8, 0)
        state 2 => position = 1.00  orange (255, 102, 0) => (1, 0.4, 0)
    """
    cdict = {'red':   ((0.00, 1.00, 1.00),
                       (0.5, 0.2588, 0.2588),
                       (1.00, 1.00, 1.00)),
             'green': ((0.00, 1.00, 1.00),
                       (0.50, 0.4118, 0.4118),
                       (1.00, 0.3764, 0.3764)),
             'blue':  ((0.00, 1.00, 1.00),
                       (0.50, 0.1843, 0.1843),
                       (1.00, 0.21, 0.21))}
    
    #Now create the colormap object
    colormap = colors.LinearSegmentedColormap('mycolors', cdict, 256)
    
    #Set up plot object    
    fig, ax = plt.subplots()
    plt.axis('scaled')
    plt.axis([0, Y, 0, X])
    
    cplot = plt.pcolormesh(z, cmap = colormap, vmin = 0, vmax = 2)
    
    plt.title('Wood bore infestation with initial density = ' + str(density) + 
              '\nGeneration 0')  
    
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
    nGen = 1
    
    #Loop until a stop condition is met
    while not stopFlag:
        #Create an array that tells number of infected trees in each trees
        #neighborhood as defined by the function call
        nBore = ndimage.generic_filter(z==2, np.sum, footprint = mask, 
                                       mode = bc_mode, output = int)
              
        #Rules rule!
        """
        States: bare (0), green tree (1), infected tree (2)
        Rules:
          rule 1: A healthy tree with n infested neighbors in step i has a 
                  probability p of becoming infested in step i+1, where 
                  p = n/10 for Moore with r = 1, p = n/30 for Moore with 
                  r = 2, p = n/5 for von Neumann with r = 1, and p = n/15 
                  for von Neumann with r = 2 

          rule 2: Sites that are bare or that contain infested trees 
                  do not change state.
        """

        #Rule 1
        
        #Based on input define probability array
        if neighborhood == 'Moore' and radius == 1:
            prob = nBore/10    
        if neighborhood == 'Moore' and radius == 2:
            prob = nBore/30
        if neighborhood == 'vonNeumann' and radius == 1:
            prob = nBore/5
        if neighborhood == 'vonNeumann' and radius == 2:
            prob = nBore/15
        
        #Determine if each tree in prob is actually infected
        infect = np.random.binomial(1, prob, (X, Y))

        #If a tree is healthy, has an infected tree in its neighborhood,
        #and was actually infected change its value in z array to 2 indicating
        #that it is infected.
        rcheck = (z == 1) & (nBore > 0)
        r1 = (z == 1) & (nBore > 0) & (infect == 1)
        z[r1] = 2


        #Convert to 1D array
        cplot.set_array(z.ravel())
        plt.title('Wood bore infestation with initial density = ' + str(density) + 
                  '\nGeneration ' + str(nGen))
        
        #Pause so the change is more readable
        plt.pause(0.2)
        
        #Stop if no trees infected
        if not (z == 2).any():
            stopFlag = True
        
        #Stop if no healthy trees remain
        if not (z == 1).any():
            stopFlag = True
        
        #Stop if no healthy trees has an infected neighbor
        if not (rcheck).any():
            stopFlag = True

        #Stop if max generation is reached
        if nGen == maxGen:
            stopFlag = True
        
        #Increase counter as next generation begins
        else:
            nGen += 1
            
    
#=============================================================================
#Self-test code
if __name__ == '__main__':
    bore(density = 0.75, neighborhood = 'vonNeumann', radius = 1, nGen = 1, 
             pbc = True, grid = False)