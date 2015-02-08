%Loading Script
%Loads all data from folder into MATLAB workspace for processing

%NOTE: Check that the file path in "FolderName" is correctly specified 
%      before running script

clear all

FolderName='Sub015_Exported_MATLAB/*mat';%Sets the file path
%/*.mat part specifies only to obtain file names with .mat in them

FileList=dir(FolderName); %Retrieves all folder names

NumFiles=size(FileList); %Determines the number of .mat files to load

for i = 1:NumFiles(1) %Iterates through each the length of FileList
    name=FileList(i).name; %Retrieves the file name of the file as a string
    filepath= strcat('Sub015_Exported_MATLAB/', name); %Concatenates the file name to form the full file path
    load(filepath) %Loads the data file

end

clear FileList filepath FolderName i name %Clears all variables created in this script