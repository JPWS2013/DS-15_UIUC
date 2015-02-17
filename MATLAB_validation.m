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
if isequal(exist('Validate', 'dir'), 7)
    rmdir('Validate', 's')
    mkdir('Validate')
    csvpath='Validate/'; %If folder already exists, set the path
else
    mkdir('Validate') %If folder doesn't exist, create one
    csvpath='Validate/';%Then set the path
end


FilePath='OriginalData/Sub001_matlab_exported/Sub001_6MW_PPAFO_0001.mat';
name='Sub001_6MW_PPAFO_0001.mat';
struct=load(FilePath); %Loads the structure file

CountLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Count'); %Establishes the path to obtain the 'counts' variable

count=eval(CountLoc);

if count > 0
    
    ind=strfind(name, 'Sub');
    PNum=num2str((name((ind+3):(ind+5))));
            
    TrialInd=strfind(name, '_00');
    TrialNum=num2str((name((TrialInd+1):TrialInd+4)));
                
    for i=1 : 3
        
        output_mat=[0,0,0,0];
        
        if i==1
            %SpaceCoord='X'
            csv_filename='Validate/validdata_x.csv'
        elseif i==2
            csv_filename='Validate/validdata_y.csv'
        elseif i==3
            csv_filename='Validate/validdata_z.csv'
        end
        
        
        LabelLoc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Labels');%Establish path to the labels
        labels=eval(LabelLoc);%Retrieves the labels
        reform_labels=[];
                
        for j = 1:length(labels)
            reform_labels=[reform_labels,labels(j), ','];
        end
                
        Label_Filename=strcat('Validate/Label.csv'); %Sets up the csv file name for the labels
        csvwrite(Label_Filename, reform_labels)%Writes the csv file for the labels
                    
        mat_loc=strcat('struct.', name(1:(length(name)-4)), '.Trajectories.Labeled.Data(:,',num2str(i),',:)');
        matrix=eval(mat_loc);
        dim=size(matrix);
                    
        for k=1:dim(1)
            MarkerName=labels{k}
            vec_raw=matrix(k,1,:);
            vec_intermediate=vec_raw(~isnan(vec_raw));
            vec=reshape(vec_intermediate, [], 1);

            Mean=mean(vec);
            Median=median(vec);
            Max=max(vec);
            Min=min(vec);

            Output= [Mean, Median, Max, Min]
            
            output_mat=cat(1, output_mat, Output)
            
            final_output=output_mat(2:end,:)
            
            csvwrite(csv_filename, final_output)
            


        end   
                
                
    end


end
