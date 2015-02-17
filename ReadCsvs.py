"""
File: ReadCsvs.py
Created on Sat Feb  7 23:57:02 2015

Code authored by Justin Poh for Data Science, Spring 2015

This module provides functions to parse the csv files created by the matlab script in order to generate the appropriate data structures
useful for further processing.
"""

import GaitClass as gc
import numpy as np
import pandas as pd
import copy

def ReadGaitData():
    FullData=FormData() #Get all the data out of the CSV files
    AFO, PPAFO, Shoes=SortbyFootwear_MT(FullData) #Process and clean the data to have a consistent number of columns with column names in the same order
    AFO_g, PPAFO_g, Shoes_g=GroupParticipants([AFO, PPAFO, Shoes])
    
    return AFO_g, PPAFO_g, Shoes_g

def GroupParticipants(SortedData):
    """
    """
    AFO_g=dict()
    PPAFO_g=dict()
    Shoes_g=dict()
    
    for i in range(3):
        for j in range(1, 17):
            gc.Participant(j)
            
            if i==0:
                AFO_g[j]=gc.Participant(j)
            
            if i==1:
                PPAFO_g[j]=gc.Participant(j)
                
            if i==2:
                Shoes_g[j]=gc.Participant(j)
    
    for i in range (3):
        
        footwear=SortedData[i]
        AllData=footwear.keys()
        
        for eachData in AllData:
            MT_Obj=footwear[eachData]
            ParticipantNum=MT_Obj.pnum
            
            if i==0:
                AFO_g[ParticipantNum].AddTrial(MT_Obj)
            
            if i==1:
                PPAFO_g[ParticipantNum].AddTrial(MT_Obj)
                
            if i==2:
                Shoes_g[ParticipantNum].AddTrial(MT_Obj)
                
    return AFO_g, PPAFO_g, Shoes_g
            
            
        
    

def CsvtoList(filepath):
    """
    This function carries out the "dirty" work of converting a set of strings in a csv written by MATLAB into a list of the strings
    
    filepath:A string that is the filepath to the csv that contains the desired information
    
    Returns a list of all the strings contained in the csv file
    """
    FnameFile = open(filepath, 'r') #Opens the csv file
    
    for line in FnameFile.readlines(): #for each line in the csv file
        t = line.split(',,') #Split the line using the ',,' as the delimiter
        del t[-1] #Removes the \n character that gets added to the end of the list
      
    for i in range(len(t)): #for every string that is in that list of strings
        eachname=t[i]
        for eachchar in eachname:#iterate through every character in that string
            if eachchar in ",":#if a character is equal to the comma
                eachname=eachname.replace(eachchar, '') #remove the comma from the list (this is to clean the string)
        t[i]=eachname #replace the original string in the list with the cleaned up one in the same position in the list
    
    return t #return the cleaned list

def FormData():
    """
    This function converts the CSV files into one 3D numpy array (ndarray) for each trial. It then stores the ndarray in an 
    instance of a gaitraw object and then stores each gaitraw object into a dictionary using the original matlab structure file 
    name as the key and the 3D numpy array as the value. 
    
    Returns a dictionary of all the GaitRaw objects representing each trial in the dataset
    """
    #NameList=CsvtoList('Csvs/fname.csv') #Retrieves the list of file names from the csv file
    NameList=['Sub001_6MW_PPAFO_0001.mat']
    FullData={}#Creates a dictionary that will store the full data
    
    for EachFile in NameList: #for each file name listed in the list of file names
        print EachFile
        label_filename='Csvs/'+EachFile[0:-4]+'_Label.csv'#create the file path to obtain the csv containing the labels for the markers
        labels=CsvtoList(label_filename) #retreive a list of the labels for the markers
    
        for i in range(5): #depending on whether you're looking for the x, y or z set of data
            if i==0: #if you're looking for the x set
                CsvName='Csvs/'+EachFile[0:-4] + '_x.csv' #create the file path to the csv containing the x set of data
                data1=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
                
            if i==1:
                CsvName='Csvs/'+EachFile[0:-4] + '_y.csv' #create the file path to the csv containing the y set of data
                data2=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
            if i==2:
                CsvName='Csvs/'+EachFile[0:-4] + '_z.csv' #create the file path to the csv containing the z set of data
                data3=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
                
            if i==3:
                CsvName='Csvs/'+EachFile[0:-4] + '_r.csv' #create the file path to the csv containing the z set of data
                data4=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
                
            if i==4:
                CsvName='Csvs/'+EachFile[0:-4] + '_attr.csv' #create the file path to the csv containing the z set of data
                data5=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
            
        dataset=np.dstack((data1, data2, data3, data4)) #stack them depth wise to form the final 3D array
        
        FullData[EachFile]=gc.GaitRaw(dataset,labels,EachFile, data5) #Initiate a GaitRaw object for each dataset and store all data sets in a dictionary with the file names as keys
        
    print "Done reading all data!"
    return FullData

def SortbyFootwear_MT(DataDict):
    """
    This function sorts the data by footwear and performs a first pass at cleaning the data by ensuring each data set contains 
    a column for all the markers, regardless of whether there is data for them or not. It also stores each trial in an instance
    of a MarkerTime object that indicates that the columns are markers, the rows are time and the depth is space coordinate.
    
    All the generated MarkerTime objects are then stored in one of three dictionaries depending on what footwear was worn.
    
    Returns a tuple of dictionaries (AFO, PPAFO, Shoes)
    """
    keys=DataDict.keys() #Retrieves all the filenames contained in the dictionary of raw data
    PPAFO_dict=dict() #Initializes a place to store the categorized PPAFO raw data
    AFO_dict=dict() #Initializes a place to store the categorized AFO raw data
    Shoes_dict=dict() #Initializes a place to store the categorized Shoes raw data
    PPAFO=dict() #Initializes a place to store the cleaned PPAFO data
    AFO=dict() #Initializes a place to store the cleaned AFO data
    Shoes=dict() #Initializes a place to store the cleaned Shoes data
    
    for DataName in keys: #for each file name in the raw data dictionary
        if 'PPAFO' in DataName: #if it has PPAFO in the file name
            PPAFO_dict[DataName]=DataDict[DataName] #file it in the PPAFO raw data dictionary
        elif 'PPAFO' not in DataName and 'AFO' not in DataName: #else if it doesn't have PPAFO or AFO in the file name
            Shoes_dict[DataName]=DataDict[DataName] #file it in the Shoes raw data dictionary 
        else: #else if it doesn't match either criteria
            AFO_dict[DataName]=DataDict[DataName] #then it must be an AFO trial so file it in the AFo raw data dictionary
    
    #Some debugging statements to help determine if the above sorting algorithm has sorted the files correctly
    #print len(PPAFO_dict.keys())
    #print len(AFO_dict.keys())
    #print len(Shoes_dict.keys())
    
    collection=[PPAFO_dict, AFO_dict, Shoes_dict] #packs up all the raw data dictionaries into a list for processing
    
    for i in range(3): #for each of the footwear conditions
        for FName in collection[i].keys(): #for each file name contained in each raw data dictionary
            print FName
        
            #FullLabelSet is a list containing the names of every possible marker in order from participant's right to participant's left in order around the legs
            FullLabelSet=['SACRAL', 'R_ASIS', 'R_TROCH', 'R_THIGH', 'R_LAT_KNEE', 'R_TIB', 'R_LAT_MAL', 'R_TOE_5', 'R_TOE_1', 'R_MED_MAL', 'R_HEEL', 'R_MED_KNEE', 'L_MED_KNEE', 'L_HEEL', 'L_MED_MAL', 'L_TOE_1', 'L_TOE_5', 'L_LAT_MAL', 'L_TIB', 'L_LAT_KNEE', 'L_TROCH', 'L_THIGH', 'L_ASIS']
            
            DataArr=collection[i][FName] #Retrieves the GaitRaw object for that file name
            Data=DataArr.data #Retrieves the 3D ndarray for that file name
            Attr=DataArr.charac #Retrieves the list of attributes for that data file 
            dimen=Data.shape #Determines the shape of the ndarray
            
            #Debugging statement to check the format of dimen
            #print "Dimen=", dimen
            
            #Initialize an empty numpy array that has as many columns as there are markers (23) and as many rows as there are time points
            init=np.empty((dimen[1], 23))  
            init[:]=np.nan #Converts all values in the initialized ndarray to NANs
            template=pd.DataFrame(data=init, columns=FullLabelSet) 
            
            X=copy.deepcopy(template) #Creates a pandas dataframe for the X spatial coordinate
            Y=copy.deepcopy(template) #Creates a pandas dataframe for the Y spatial coordinate
            Z=copy.deepcopy(template) #Creates a pandas dataframe for the Z spatial coordinate
            R=copy.deepcopy(template) #Creates a pandas dataframe for the R spatial coordinate
            
            
            for label in FullLabelSet: #for each label in the FullLabelSet
                lab=DataArr.labels #Retrieve the labels stored in the GaitRaw object for each trial
                if label in lab: #if the trial had that marker identified
                    RowIndex=lab.index(label) #find out which row the data for that marker was stored in

                    X[label]=Data[RowIndex,:,0].tolist() #Get the data for that marker from the 1st plane of the 3D ndarray
                    Y[label]=Data[RowIndex,:,1]#Get the data for that marker from the 2nd plane of the 3D ndarray
                    Z[label]=Data[RowIndex,:,2]#Get the data for that marker from the 3rd plane of the 3D ndarray
                    R[label]=Data[RowIndex,:,3]#Get the data for that marker from the 3rd plane of the 3D ndarray
                    
                    #Debug statement to check the length of the data being retrieved                    
                    #print len(Data[RowIndex,:,0])
            
            res=gc.MarkerTime(FName, X, Y, Z, R, Attr) #store the three pandas dataframes into a MarkerTime object representing that trial
            
            if i==0:
                res.fw='PPAFO'
#                print "File Name =", res.name
#                print "pnum=", res.pnum   
#                print "footwear=", res.fw
#                print "trial number =", res.trial
                
                PPAFO[FName]=res #if we're working with PPAFO trials, store the MarkerTime object in the PPAFO dictionary
            
            if i==1:
                res.fw='AFO'
#                print "File Name =", res.name
#                print "pnum=", res.pnum   
#                print "footwear=", res.fw
#                print "trial number =", res.trial
                
                AFO[FName]=res #if we're working with AFO trials, store the MarkerTime object in the AFO dictionary
            
            if i==2:
                res.fw='Shoes'
#                print "File Name =", res.name
#                print "pnum=", res.pnum   
#                print "footwear=", res.fw
#                print "trial number =", res.trial
                
                Shoes[FName]=res #if we're working with Shoes trials, store the MarkerTime object in the Shoes dictionary
            
            
            
    return AFO, PPAFO, Shoes #return the three dictionaries as a tuple
   
if __name__ == '__main__':
    
    
    AFO, PPAFO, Shoes=ReadGaitData()    
    
    #print AFO.keys()
    #print AFO[1]
    #print AFO[1].ShowTrials()
    #print AFO[1].GetTrial(1)
    
    
    #Some debug statements to check that each clean data dictionary has the right number of trials in them
#    print len(AFO.keys())
#    print AFO[AFO.keys()[0]].r
#    print len(PPAFO.keys())
#    print len(Shoes.keys())