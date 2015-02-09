"""
File: GaitClass.py
Created on Sat Feb  7 23:57:02 2015

Code authored by Justin Poh for Data Science, Spring 2015

This module provides the implementation called GaitClass that provides a customized data structure to store the 3D array format
of the original data in a way that makes sense to in order to obtain Pandas Arrays
"""

class GaitData:
    """
    This class creates an object that represents 1 participant in the data
    """
    def __init__(self, Participant, AFO, PPAFO, Shoes):
        self.pnum=Participant
        self.afo=AFO
        self.ppafo=PPAFO
        self.shoes=Shoes

class MarkerTime(GaitData): 
    """
    This class creates an object that represents the cleaned data from 1 trial
    """    
    def __init__(self, Label, X, Y, Z):
       self.name=Label
       self.x=X
       self.y=Y
       self.z=Z
   
    def AddStructure(self, pd, label):
       self.data[label]=pd

        
class GaitRaw:
    """
    This class creates an object that represents the raw data from 1 trial
    """
    def __init__(self, dat,Labels,Name='None'):
        self.name=Name
        self.labels=Labels
        self.data=dat
        
    