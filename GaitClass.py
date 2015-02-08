"""
File: GaitClass.py
Created on Sat Feb  7 23:57:02 2015

Code authored by Justin Poh for Data Science, Spring 2015

This module provides the implementation called GaitClass that provides a customized data structure to store the 3D array format
of the original data in a way that makes sense to in order to obtain Pandas Arrays
"""

class GaitData:
    
    def __init__(self, name):
        self.label=name
        self.data=dict()
        
    
    def AddStructure(self, pd, label):
        self.data[label]=pd
        
class GaitRaw:
    
    def __init__(self, dat,Labels,Name='None'):
        self.name=Name
        self.labels=Labels
        self.data=dat