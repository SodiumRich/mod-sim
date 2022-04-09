# -*- coding: utf-8 -*-
"""
Random snake
Multiple random snakes on a 2D lattice, show path for each snake
Each site on grid can only be moved to when no snake is present there

Created: 2020-04-04
Last modified: 2021-04-08

@author: jim.rathman, Tanner Kirk

Outside Help: Ben Pung: General Syntax, Explained how self vs not self
                variables work, printing syntax
              Rachel Jarzemba: Explained algorithm for reseting location array,
                              I had been deleting the last spot of the tail too
                              early resulting in snakes running over themselves
"""

import random
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================

#Define Snake Class
class snake:
    
    #snake defined by initial position, head symbol, color, direction facing,
    #and length
    def __init__(self, position=(10, 10), symbol='o', color='b',\
                 direction='north', length=5):
        """
        Parameters
        ----------
        Position : TYPE: tuple of ints
            DESCRIPTION: Initial Head Position
            
        Symobl : TYPE: string
            DESCRIPTION: Define Head Symbol 
            
        Color : TYPE: string
            DESCRIPTION: Define Snake Color 
        
        Direction : TYPE: string
            DESCRIPTION: Initial Snake Direction 'north', 'south', 'east', 
            'west'    
        
        length : TYPE: int
            DESCRIPTION: Number of Segments in Snake 
            
        
        Initialize snake given defined characteristics. Will determine initial 
        location of tail segments.
        
        """
        
        #Define Initial Values
        self.length = length
        self.symbol = symbol
        self.color = color
        self.direction = direction
        self.trapped = False
        
        #Initial xpos and ypos arrays, length + 1 because five segments means 
        #six nodes
        self.xpos = [0]*(length + 1)
        self.ypos = [0]*(length + 1)

        #Set head position as first index in pos arrays
        self.xpos[0] = position[0]
        self.ypos[0] = position[1]

        #Set other initial values in position arrays based on direction faced
        if self.direction == 'north':
            for i in range(self.length):
                self.xpos[i+1] = self.xpos[0]
                self.ypos[i+1] = self.ypos[0] - (i+1)

        if self.direction == 'south':
            for i in range(self.length):
                self.xpos[i+1] = self.xpos[0]
                self.ypos[i+1] = self.ypos[0] + (i+1)

        if self.direction == 'east':
            for i in range(self.length):
                self.xpos[i+1] = self.xpos[0] - (i+1)
                self.ypos[i+1] = self.ypos[0]

        if self.direction == 'west':
            for i in range(self.length):
                self.xpos[i+1] = self.xpos[0] + (i+1)
                self.ypos[i+1] = self.ypos[0]

    #Define move, include max x and y based on grid size, boundary condition,
    #and the location of the snake currently
    def move(self, xmax, ymax, bc, snakePresent):
        """

        Parameters
        ----------
        xmax : TYPE: int
            DESCRIPTION: Max X coordinate determined by grid size
            
        ymax : TYPE: int
            DESCRIPTION: Max Y coordinate determined by grid size 
            
        bc : TYPE: string
            DESCRIPTION: Define boundary condition. 'wall' or 'periodic'
            Wall indicates a hard wall the snake cannot pass through
            Periodic indicates a wall that once passed through the snake will
            appear at opposite wall
        
        snakePresent : boolean array
            DESCRIPTION: Defines if a snake is present at any given location 
            in the grid
            
        Move the snake
        

        """
        
        # For each boundary condition option ('wall' or 'periodic'), given a
        # snake currently at position (xpos, ypos), determine which directions
        # for the next move are disallowed because the site has already been
        # snakePresent.
        
        #Empty set object; will add disallowed directions
        disallowed = set()

        #Decide which directions are not allowed based on head location in
        #relation to wall and position of snake body
        
        if bc == 'wall':
            if self.ypos[0] == ymax or snakePresent[self.xpos[0], self.ypos[0]+1]:
                disallowed.add('north')
            if self.xpos[0] == xmax or snakePresent[self.xpos[0]+1, self.ypos[0]]:
                disallowed.add('east')
            if self.ypos[0] == 0 or snakePresent[self.xpos[0], self.ypos[0]-1]:
                disallowed.add('south')
            if self.xpos[0] == 0 or snakePresent[self.xpos[0]-1, self.ypos[0]]:
                disallowed.add('west')
        elif bc == 'periodic':
            if (self.ypos[0] == ymax and snakePresent[self.xpos[0], (self.ypos[0]+1) % ymax]) \
                    or (self.ypos[0] < ymax and snakePresent[self.xpos[0], self.ypos[0]+1]):
                disallowed.add('north')
            if (self.xpos[0] == xmax and snakePresent[(self.xpos[0]+1) % xmax, self.ypos[0]]) \
                    or (self.xpos[0] < xmax and snakePresent[self.xpos[0]+1, self.ypos[0]]):
                disallowed.add('east')
            if (self.ypos[0] == 0 and snakePresent[self.xpos[0], (self.ypos[0]-1) % ymax]) \
                    or (self.ypos[0] > 0 and snakePresent[self.xpos[0], self.ypos[0]-1]):
                disallowed.add('south')
            if (self.xpos[0] == 0 and snakePresent[(self.xpos[0]-1) % xmax, self.ypos[0]]) \
                    or (self.xpos[0] > 0 and snakePresent[self.xpos[0]-1, self.ypos[0]]):
                disallowed.add('west')

        #Use the set method 'difference' to get set of allowed directions
        allowed = {'north', 'east', 'south', 'west'}.difference(disallowed)

        #If no directions allowed snake is trapped
        if len(allowed) == 0:
            self.trapped = True

        else:
            """
            Randomly pick from the allowed directions; need to convert set
            object to a list because random.choice doesn't work on sets
            """

            self.direction = random.choice(list(allowed))

            #Insert current head location at front of position arrays
            self.xpos.insert(0, self.xpos[0])
            self.ypos.insert(0, self.ypos[0])

            #Depending on new direction add to correct position array to
            #reflect movement of snake head
            #Tail will be deleted later
            if self.direction == 'north':
                if (bc == 'wall' and self.ypos[0] < ymax) or bc == 'periodic':
                    self.ypos[0] += 1

            elif self.direction == 'east':
                if (bc == 'wall' and self.xpos[0] < xmax) or bc == 'periodic':
                    self.xpos[0] += 1

            elif self.direction == 'south':
                if (bc == 'wall' and self.ypos[0] > 0) or bc == 'periodic':
                    self.ypos[0] -= 1

            elif self.direction == 'west':
                if (bc == 'wall' and self.xpos[0] > 0) or bc == 'periodic':
                    self.xpos[0] -= 1

            """
            With periodic boundary conditions, it's possible that (xpos, ypos) could
            be off the grid (e.g., xpos < 0 or xpos > xmax). The Python modulo
            operator can be used to give exactly what we need for periodic bc. For
            example, suppose xmax = 20; then if xpos = 21, 21 % 20 = 1; if xpos = -1,
            -1 % 20 = 19. (Modulo result on a negative first argument may seem
            strange, but it's intended for exactly this type of application. Cool!)
            If 0 <= xpos < xmax, then modulo simply returns xpos. For example,
            0 % 20 = 0, 14 % 20 = 14, etc. Only special case is when xpos = xmax, in
            which case we want to keep xpos = xmax and not xpos % xmax = 0
            """
            if self.xpos[0] != xmax:
                self.xpos[0] = self.xpos[0] % xmax
            if self.ypos[0] != ymax:
                self.ypos[0] = self.ypos[0] % ymax

# =============================================================================

#Grid class
class Grid:
    
    #Initialized with snakes, max gridsize, boundary conditions, and max
    #number of steps allowed
    def __init__(self, snakes, gridsize=(20, 20), bc='wall', steps=250):
        '''
        

        Parameters
        ----------
        snakes : Tuple of Snakes
            Contains all initialized snakes in a single tuple
        gridsize : TYPE Tuple of two ints, optional
            DESCRIPTION. The size of the grid given as (x,y) 
            The default is (20, 20).
        bc : string, optional
            DESCRIPTION. Define boundary condition. 'wall' or 'periodic'
            Wall indicates a hard wall the snake cannot pass through
            Periodic indicates a wall that once passed through the snake will
            appear at opposite wall The default is 'wall'.
        steps : Int, optional
            DESCRIPTION. Define the max number of movements allowed
            The default is 250.

        Returns
        -------
        None.

        '''
        
        #initialize values
        self.snakes = snakes
        self.xmax = gridsize[0]
        self.ymax = gridsize[1]
        self.bc = bc
        self.point = []
        
        #Max Steps
        self.steps = steps
        
        #Step counter
        self.m = 0

        #Array to keep track of points that have been snakePresent
        self.snakePresent = np.zeros([self.xmax + 1, self.ymax + 1], dtype=bool)

        #Create new figure window if one is already open
        plt.figure()
        ax = plt.axes(xlim=(0, self.xmax), ylim=(0, self.ymax))

        #For each snake do the following
        for s in self.snakes:

            #Plot head location using symbol
            self.head, = ax.plot(s.xpos[0], s.ypos[0], s.symbol, color=s.color)
            
            #Plot body line using rest of position array
            self.body, = ax.plot(s.xpos, s.ypos, color=s.color)

            #Set snakePresent to true for location of each snake
            for i in range(len(s.xpos)):
                self.snakePresent[s.xpos[i], s.ypos[i]] = True

            #Combine all snake locations into point
            self.point.append([self.head, self.body])

        #Figure title
        plt.title('Multiple snakes')

    #Def go
    def go(self):
        """
        Tracks movements of snakes

        Returns
        -------
        None.

        """
        #While all snakes are not trapped and while number of steps is less
        #max steps
        while ((not all([s.trapped for s in self.snakes])) and (self.m < self.steps)):
            
            #Reset snakePresent to false for all locations
            self.snakePresent = np.zeros([self.xmax + 1, self.ymax + 1], dtype=bool)

            #Update snake location for each snake
            for s in self.snakes:
                self.snakePresent[s.xpos[:],s.ypos[:]] = True
            
            #For each snake i = 0,1,2
            for i, s in enumerate(self.snakes):

                #Move snake passing snakePresent to disallow certain directions
                s.move(self.xmax, self.ymax, self.bc, self.snakePresent)
                
                #After move set new head location to true
                self.snakePresent[s.xpos[0],s.ypos[0]] = True
                
                #After move set previous final tail location to False
                self.snakePresent[s.xpos[-1],s.ypos[-1]] = False
                
                #Remove final Tail location
                s.xpos.pop()
                s.ypos.pop()

                #If snake is not trapped
                if not s.trapped:
                    
                    #Update point for head location
                    self.point[i][0].set_data(s.xpos[0], s.ypos[0])
                    
                    #Update point for tail location
                    self.point[i][1].set_data(s.xpos, s.ypos)
                    
            #Increase step counter by 1
            self.m += 1            
            plt.pause(0.2)
            
# main program=================================================================
iggy = snake(position=(5, 5), symbol='^', color='m', direction='east', length = 5)
ivey = snake(position=(15, 15), symbol='d', color='r', direction='west', length = 12)
igor = snake(position=(5, 15), symbol='o', color='g')
snakes = (iggy, ivey, igor)
rwalk = Grid(snakes, gridsize=(35, 35), bc='wall')
rwalk.go()
