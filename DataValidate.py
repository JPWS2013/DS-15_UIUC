"""
File: DataValidate.py
Created on Sat Feb  7 23:57:02 2015

Code authored by Justin Poh and Julianne Jorgensen for Data Science, Spring 2015

This module provides functions to validate the pipeline using validation data generated in matlab
"""
import ReadCsvs as rc
import os
import numpy as np
import sys

def ValidationTest(GaitData, fw, PNum, TrialNum):
    
    X, Y, Z, labels = ReadMatLabOutput()
    
    p_dict=GaitData[fw]

    participant=p_dict[PNum]

    trial=participant.trials[TrialNum]
    
    print "PNum ", trial.pnum
    print "Trial ", trial.trial
    print "Footwear", trial.fw

    X_df=trial.x
    Y_df=trial.y
    Z_df=trial.z    
    
    for i in range(len(labels)):
        
        label=labels[i]
        
        for j in range(3):
            
            if j ==0:
                truth_series=X_df[label]
                ToCheck=X[i]
            if j ==1:
                truth_series=Y_df[label]
                ToCheck=Y[i]
            if j ==2:
                truth_series=Z_df[label]
                ToCheck=Z[i]
                
            truth=[truth_series.mean(), truth_series.median(), truth_series.max(), truth_series.min()]
            
            for k in range(len(ToCheck)):
                
                eachCheck = ToCheck[k]
                eachTruth = truth[k]
                if abs(round(eachCheck,2) - round(eachTruth,2)) > 0.011:
                    
                    print "ERROR FOUND!!"
                    print "Label=", label
                    print "eachCheck =", round(eachCheck,2)
                    print "eachTruth =", round(eachTruth, 2)
                    print abs(round(eachCheck,2) - round(eachTruth,2))
                    sys.exit()
                    
                #print abs(round(eachCheck,2) - round(eachTruth,2))
                        
        #print "Label", label, "has passed tests"
    
    print "Tests complete, all passed!"
                        

def ReadMatLabOutput():
        
    FileList=os.listdir('Validate')
    
    for name in FileList:
        if 'validdata' in name:
            FilePath='Validate/' + name
            print FilePath
            data1=np.genfromtxt(FilePath, delimiter=',')
            
            if '_x' in name:
                X=data1
            
            if '_y' in name:
                Y=data1
                
            if '_z' in name:
                Z=data1

    label_filename='Validate/Label.csv' #create the file path to obtain the csv containing the labels for the markers
    labels=rc.CsvtoList(label_filename)
    
    return X, Y, Z, labels
    
if __name__ == '__main__':
        data=rc.ReadGaitData()
        ValidationTest(data, 1,1,1)