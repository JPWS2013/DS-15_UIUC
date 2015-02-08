"""
File: ReadCsvs.py
Created on Sat Feb  7 23:57:02 2015

Code authored by Justin Poh for Data Science, Spring 2015

This module provides functions to parse the csv files created by the matlab script in order to generate the appropriate data structures
useful for further processing.
"""

import GaitClass as gc
import numpy as np

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

NameList=CsvtoList('Csvs/fname.csv') #Retrieves the list of file names from the csv file
FullData={}#Creates a dictionary that will store the full data

for EachFile in NameList: #for each file name listed in the list of file names
    label_filename='Csvs/'+EachFile[0:-4]+'_Label.csv'#create the file path to obtain the csv containing the labels for the markers
    labels=CsvtoList(label_filename) #retreive a list of the labels for the markers

    for i in range(3): #depending on whether you're looking for the x, y or z set of data
        if i==0: #if you're looking for the x set
            CsvName='Csvs/'+EachFile[0:-4] + '_x.csv' #create the file path to the csv containing the x set of data
            data1=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
            
        if i==1:
            CsvName='Csvs/'+EachFile[0:-4] + '_y.csv' #create the file path to the csv containing the y set of data
            data2=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
        if i==2:
            CsvName='Csvs/'+EachFile[0:-4] + '_z.csv' #create the file path to the csv containing the z set of data
            data3=np.genfromtxt(CsvName, delimiter=',') #generate a numpy array from the data in that csv
        
    dataset=np.dstack((data1, data2, data3)) #stack them depth wise to form the final 3D array
    
    FullData[EachFile]=gc.GaitRaw(dataset,labels,EachFile) #Initiate a GaitRaw object for each dataset and store all data sets in a dictionary with the file names as keys
    

#This is just testing script that can be used to verify the data array has the right shape
keys=FullData.keys()

print FullData[keys[1]].name
print FullData[keys[1]].data.shape