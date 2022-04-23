# -*- coding: utf-8 -*-
"""
Cellular Automata

Created:2016-11-14
Last modified: 2020-04-15
@author: jrathman
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#import matplotlib.ticker as ticker

def ant(nGen = 11400, nAnt = 1, N = 100):
    """
    Interesting example of a cellular automation that exhibits three phases:
    simple patterns, chaos, emergent periodic order (which appears after
    about 10,000 steps for the single-ant case below). Rules for this CA apply 
    only to the current cell; neighboring cells have no influence and therefore 
    we don't need to specify a neighborhood.
    
    The two ant case is also very cool. For a particular initial positioning of 
    both ants, they move and form a complex chaotic pattern and then slowly start 
    undoing the pattern until they return to the initial condition and it starts 
    all over again. One interesting aspect of this CA is that multiple ants can 
    occupy the same cell without conflict because the rules are never in conflict. 
    An incredibly complex but weirdly periodic system!
    
    For the initial states used here, note that the pattern created by the
    left ant is a bit higher than the pattern of the right ant. The patterns
    merge but then at around 9000 steps become separate, and then at about
    11,100 steps both patterns simultaneously return to just one or two black
    cells... and then they start again, this time with the pattern of the
    right ant being a bit higher than the left ant. Again, the patterns grow,
    merge, separate, and finally shrink away to nearly nothing at about
    23,000 steps, and then away we go again. Periodicity!
    
    Parameters:
        nGen: number of generations
        nAnt: number of ants (1 or 2)
        N: grid size
    """

    #Drop the ant
    if nAnt == 1:
        direction = ['north']
        xpos = [3*N//5] #horizontal location
        ypos = [3*N//5] #vertical location
    elif nAnt == 2:
        direction = ['north', 'east']
        xpos = [N//2 - N//8 - 1, N//2 + N//8 + 1]
        ypos = [N//2, N//2]
    else:
        raise ValueError('nAnt must be 1 or 2')
    
    z = np.zeros((N, N), dtype = int) #add boundary rows and columns
        
    """
    Define colormap to use. Can pick from the many built-in colormaps, or,
    as shown below, create our own. First create a dictionary object with
    keys for red, green, blue. The value for each pair is a tuple of tuples.
    Must have at least 2 tuples per color, but can as many as you wish. The
    first element in each tuple is the position on the colormap, ranging from
    0 (bottom) to 1 (top). The second element is the brightness (gamma) of the
    color. The third element is not used when we only have two tuples per color.
    The conventional red-green-blue (RGB) color scale has gamma values ranging
    from 0 to 255 (256 total levels); these are normalized 0 to 1. I.e., a gamma
    of 1 in the color tuple denotes gamma 255. In the colormap defined here,
    the bottom level color is white (the second element for all three colors is
    1) and the top level is purple (0, 204, 0) => (0, 0.8, 0)
    """
    cdict = {'red':   ((0.0, 1.00, 1.00),
                       (1.0, 0.60, 0.60)),
             'green': ((0.0, 1.00, 1.00),
                       (1.0, 0.00, 0.00)),
             'blue':  ((0.0, 1.00, 1.00),
                       (1.0, 0.80, 0.80))}
    
    #Now create the colormap object
    colormap = colors.LinearSegmentedColormap('mycolors', cdict, 256)
    
    #Set up plot object    
    fig, ax = plt.subplots()
    plt.axis('scaled')
    plt.axis([0, N, 0, N])
    
    """
    pcolormesh creates a quadmesh object. vmin and vmax specify the min and
    max values in z. If these are not specified, then if z is all zeros (or
    all ones), then plot won't work because function doesn't know what color
    to use if all values are the same.
    """
    
    cplot = plt.pcolormesh(z, cmap = colormap, vmin = 0, vmax = 1) 

    plt.title('Generation 0') 
    
    #Adding gridlines seems a bit more complicated than it should be...
    #Don't add grids for this one - adding grids slows sim down significantly
#    plt.grid(True, which = 'both', color = '0.5', linestyle = '-')
#    plt.minorticks_on()
#    minorLocator = ticker.MultipleLocator(1)
#    ax.xaxis.set_minor_locator(minorLocator)
#    ax.yaxis.set_minor_locator(minorLocator)
     
    #Define update function to be used to animate the plot
    for n in range(nGen+1):
        #nonlocal direction, xpos, ypos
        
        #Plot current generation        
        cplot.set_array(z.ravel()) #set_array requires a 1D array (no idea why...)
        plt.title('Generation ' + str(n))
        plt.pause(0.02)
        #print(xpos, ypos, z[xpos, ypos], np.sum(z))
        #Rules rule!
        """
        Rules:
        
        Note: In the z matrix, row numbers go from top to bottom but are plotted
        in the cell plot from bottom to top so increasing row number corresponds
        to moving northward. Col indices increase from left to right (west to east).
        In the cell plot, if xpos denotes horizontal position and ypos vertical 
        position,then this corresponds to z[ypos, xpos]
        """

        for i in range(nAnt):       
            if z[ypos[i], xpos[i]] == 0:
                z[ypos[i], xpos[i]] = 1
                if direction[i] == 'north':
                    direction[i] = 'east'
                    xpos[i] += 1
                elif direction[i] == 'east':
                    direction[i] = 'south'
                    ypos[i] -= 1
                elif direction[i] == 'south':
                    direction[i] = 'west'
                    xpos[i] -= 1
                elif direction[i] == 'west':
                    direction[i] = 'north'
                    ypos[i] += 1
            elif z[ypos[i], xpos[i]] == 1:
                z[ypos[i], xpos[i]] = 0
                if direction[i] == 'north':
                    direction[i] = 'west'
                    xpos[i] -= 1
                elif direction[i] == 'west':
                    direction[i] = 'south'
                    ypos[i] -= 1
                elif direction[i] == 'south':
                    direction[i] = 'east'
                    xpos[i] += 1
                elif direction[i] == 'east':
                    direction[i] = 'north'
                    ypos[i] += 1
