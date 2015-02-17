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
    def __init__(self, AFO, PPAFO, Shoes):
        self.afo=AFO
        self.ppafo=PPAFO
        self.shoes=Shoes

class Participant:
    
    def __init__(self, ParticipantNum):
        self.pnum=ParticipantNum
        self.trials=dict()
        
    def AddTrial(self, TrialObj):
        self.trials[TrialObj.trial]=TrialObj
        
    def ShowTrials(self):
        return self.trials.keys()
        
    def NumTrials(self):
        return len(self.trials.keys())
    
    def GetTrial(self, TrialNum):
        return self.trials[TrialNum]
        
    def __str__(self):
        
        message="There are " + str(self.NumTrials()) + " trials for Participant " + str(self.pnum) + " stored here."
        
        return str(message)

class MarkerTime(GaitData): 
    """
    This class creates an object that represents the cleaned data from 1 trial
    """    
    def __init__(self, Label, X, Y, Z, R, characteristics, footwear=None):
       
       self.name=Label
       self.trial=int(characteristics[4])
       self.fw=footwear
       self.pnum=int(characteristics[0])
       self.frames=int(characteristics[1])
       self.framerate=int(characteristics[2])
       self.count=int(characteristics[3])
       self.x=X
       self.y=Y
       self.z=Z
       self.r=R
   
    def AddStructure(self, pd, label):
       self.data[label]=pd
       
    def GetData(self, plane):
        if plane=='x':
            return self.x
            
        if plane=='y':
            return self.y
            
        if plane=='z':
            return self.z
       
    def __str__(self):
        
        message="This data is for trial number " + str(self.trial) + " for Participant " + str(self.pnum) + " who was wearing " + str(self.fw) + "." 

        return str(message)

        
class GaitRaw:
    """
    This class creates an object that represents the raw data from 1 trial
    """
    def __init__(self, dat,Labels,Name, characteristics):
        self.name=Name
        self.labels=Labels
        self.data=dat
        self.charac=characteristics
        
    