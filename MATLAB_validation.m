% File Name: MATLAB_validation.m
% Code authored by Justin Poh for Olin College Data Science, Spring 2015
% ------------------------------------------
% This file ensures that the data does not change as it is passed from
% MATLAB to python.
% ------------------------------------------
% Run this file in order to validate the MATLAB to python pipeline
% ------------------------------------------

clear all
%Checks for the folder to put the CSVs in
if isequal(exist('Csvs', 'dir'), 7)
    csvpath='Csvs/'; %If folder already exists, set the path
else
    mkdir('Csvs') %If folder doesn't exist, create one
    csvpath='Csvs/';%Then set the path
end

%Sets up the error information holders to report trals with missing data
ErrorCount=0; %Counts the number of structures with missing data
ErrorList=[]; %List of all the structures with missing data

SummDat=[];%Creates a Data Summary list that contains summary data about data sizes

FName=[];%Creates a list of all the file names

%Sets the file path
%/*.mat part specifies only to obtain file names with .mat in them
SubFolderPath='OriginalData';%Sets the file path for the folder containing the data
SubFolders=dir(SubFolderPath); %Retrieves all subfolder names
NumSubFolders=size(SubFolders); %Determines the number of subfolders that contain data

for j = 1:NumSubFolders(1) %for each subfolder
    
    SubFolderName=SubFolders(j).name; %Gets name of subfolder
    
    % Only folders that are of the form "Sub00X....." are valid. Also,
    % Subject 006 is eliminated from the data set
    
    if isempty(strfind(SubFolderName, 'Sub')) ~= true && isempty(strfind(SubFolderName, 'Sub006')) ~= false %Checks to ensure that the folder is a valid data folder
        FolderName=strcat(SubFolderPath, '/', SubFolderName, '/*.mat'); %Sets up the file path for retrieving the data files from that folder
        
        FileList=dir(FolderName); %Retrieves all names of data files
        
        NumFiles=size(FileList); %Determines the number of .mat files to load
        
        for i = 1:NumFiles(1) %for each data file
            name=FileList(i).name; %Retrieves the file name as a string
            SummDat=[SummDat, cellstr(name)]; %Adds the file to the summary data list
            filepath= strcat(SubFolderPath, '/', SubFolderName, '/', name); %Creates the full file path to the data file
            struct=load(filepath); %Loads the structure file
            CountLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Count'); %Establishes the path to obtain the 'counts' variable
            FrameRateLoc=strcat('struct.', name(1:(length(name)-4)), '.FrameRate'); %Establishes the path to obtain the 'FrameRate' variable
            FramesLoc=strcat('struct.', name(1:(length(name)-4)), '.Frames'); %Establishes the path to obtain the 'Frames' variable

            hist(struct); %The histogram of the data
        end
    end
end

