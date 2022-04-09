# -*- coding: utf-8 -*-
"""
Element and Molecule

Created:  2022-03-08
Last modified: 2022-03-08

@author: Tanner Kirk

Outside Help: Jodie Lawson - How to access Element in Molecule Line 75-76
"""

#Define Element Class
class Element:
    
    #Define Constructor
    def __init__(self, symbol):
        
        #Set Symbol to Provided
        self.symbol = symbol
        
        #Set rest of variables based on Symbol
        if symbol == 'C':
            self.name = 'Carbon'
            self.atomic_number = 6
            self.atomic_mass = 12.011
                    
        if symbol == 'H':
            self.name = 'Hydrogen'
            self.atomic_number = 2
            self.atomic_mass = 1.008
                    
        if symbol == 'O':
            self.name = 'Oxygen'
            self.atomic_number = 8
            self.atomic_mass = 15.999
                    
        if symbol == 'N':
            self.name = 'Nitrogen'
            self.atomic_number = 7
            self.atomic_mass = 14.007
                    
        if symbol == 'S':
            self.name = 'Sulfur'
            self.atomic_number = 16
            self.atomic_mass = 32.06
                    
        if symbol == 'F':
            self.name = 'Fluorine'
            self.atomic_number = 9
            self.atomic_mass = 18.998
                    
        if symbol == 'Cl':
            self.name = 'Chlorine'
            self.atomic_number = 17
            self.atomic_mass = 35.45
                    
        if symbol == 'Br':
            self.name = 'Bromine'
            self.atomic_number = 35
            self.atomic_mass = 79.904
    
    #Def str to return name symbol and atomic mass
    def __str__(self):
        return '{} ({}) {}'.format(self.name,self.symbol,self.atomic_mass)


#Define Molecule Class
class Molecule():
    
    #Define Constructor
    def __init__(self, eDict, name = None):
        
        #Set intial variables
        self.eDict = eDict
        
        self.name = name
        
        #Set Molecular weight by calling method calc.mw()
        self.mw = self.calc_mw()
        
    #Define calc_mw method
    def calc_mw(self):
        
        #Initialize mw as zero
        mw = 0.0
        
        #Iterate through eDict
        for atom in self.eDict:
            
            #Initialize an alement class using the atom from eDict
            element = Element(atom)
            
            #Withdraw the element mass and multiply by number of that atom
            #in eDict
            mw += (element.atomic_mass * self.eDict[atom])
            
        #Return molecule molecular weight
        return mw
    
        
    def __str__(self):
        
        #Initialize new symbol variable
        betterSymbol = ''
        
        #Iterate through edict making new symbol
        for atom, number in self.eDict.items():
            
            #Append the Molecule
            betterSymbol += atom
            
            #Append the Number of that molecule as a string
            betterSymbol += str(number)
        
        #Return Name, Better Symbol and Molecular weight to 4 decimal places
        return '{} ({}) MW = {:0.4f}'.format(self.name,betterSymbol,self.mw)
                   