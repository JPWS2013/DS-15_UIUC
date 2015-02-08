%File Name: MlabProcess.m
%Code authored by Justin Poh for Olin College Data Science, Spring 2015
%------------------------------------------
%This file loads all data from folder into MATLAB workspace for processing
%and writes all data to csv files for python to process
%------------------------------------------
%Run this file in order to process all necessary data
%Once all csv files are written, the script will clear the workspace
%------------------------------------------
%NOTE: Check that the file path in "FolderName" is correctly specified 
%      before running script
%------------------------------------------

clear all

%Sets the file path
%/*.mat part specifies only to obtain file names with .mat in them
FolderName='Sub015_Exported_MATLAB/*mat';%Sets the file path


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

%Actual processing starts here
FileList=dir(FolderName); %Retrieves all folder names

NumFiles=size(FileList); %Determines the number of .mat files to load

for i = 1:NumFiles(1) %Iterates through each the length of FileList
    name=FileList(i).name; %Retrieves the file name of the file as a string
    SummDat=[SummDat, cellstr(name)];
    filepath= strcat('Sub015_Exported_MATLAB/', name); %Concatenates the file name to form the full file path
    struct=load(filepath); %Loads the structure file
    CountLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Count'); %Establishes the path to obtain the 'counts' variable
    
    count=eval(CountLoc);%Obtains the value stored in the 'counts' variable
    
    if count>0 %Checks to see if there is the data we want in the structure
        FName=[FName, name,','];
        DataLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Data'); %Establish path to the data
        data=eval(DataLoc); %Retrieve the data
        
        LabelLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Labels');%Establish path to the labels
        labels=eval(LabelLoc);%Retrieves the labels
        reform_labels=[];
        for k = 1:length(labels)
            reform_labels=[reform_labels,labels(k), ','];
        end
        
        Label_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_Label.csv'); %Sets up the csv file name for the labels
        csvwrite(Label_Filename, reform_labels)%Writes the csv file for the labels
        
        StructDim=size(data); %Gets the size of the data structure
        SummDat=[SummDat,',', num2str(StructDim(1)),',', num2str(StructDim(3)),','];
        
        for j = 1 : (StructDim(2)-1) %For each slice of the 3D array (i.e. x or y or z)
            set=data(:,j,:); %Retrieves the slice of the array
            if j==1%Sets the file name of the csv based on whether the array represents the x, y or z data
                Data_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_x.csv');
            elseif j==2
                Data_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_y.csv');
            elseif j==3
                Data_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_z.csv');
            end
            
            csvwrite(Data_Filename, set) %Writes the csv file for each slice of the data set
        end
        

    else %If data is missing, flag it in the error variables
        ErrorCount=ErrorCount+1; %Increment the error count by one to indicate error found
        ErrorList=[ErrorList, name];%Add the structure name to the list
    end
    
    
    

end

csvwrite('Csvs/summarystats.csv', SummDat)%Writes a text file that provides the sizes of the arrays for validation
csvwrite('Csvs/fname.csv', FName)%Writes a text file that provides the names of all the files for python
ErrorCount
ErrorList

%clear all