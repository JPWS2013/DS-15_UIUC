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

ErrorCount=0;
ErrorList=[];

%Actual processing starts here

FileList=dir(FolderName); %Retrieves all folder names

NumFiles=size(FileList); %Determines the number of .mat files to load

for i = 1:NumFiles(1) %Iterates through each the length of FileList
    name=FileList(i).name; %Retrieves the file name of the file as a string
    filepath= strcat('Sub015_Exported_MATLAB/', name); %Concatenates the file name to form the full file path
    struct=load(filepath); %Loads the data file 
    CountLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Count');
    
    count=eval(CountLoc);
    
    if count>0
        DataLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Data');
        data=eval(DataLoc);
        
        LabelLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Labels');
        labels=eval(LabelLoc);
        Label_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_Label.csv');
        csvwrite(Label_Filename, labels)
        
        StructDim=size(data);
        
        for j = 1 : (StructDim(2)-1)
            set=data(:,j,:);
            if j==1
                Data_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_x.csv');
            elseif j==2
                Data_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_y.csv');
            elseif j==3
                Data_Filename=strcat('Csvs/',name(1:(length(name)-4)), '_z.csv');
            end
            
            csvwrite(Data_Filename, set)
        end
        

    else
        ErrorCount=ErrorCount+1;
        ErrorList=[ErrorList, name];
    end
    
    
    

end

ErrorCount
ErrorList