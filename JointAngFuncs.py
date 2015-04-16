# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:16:58 2015

@author: jpoh
"""

import math
import numpy as np
import thinkplot
import thinkstats2

def JointAngles(AFO, PPAFO, Shoes, fw, pnum, trial, mark1, mark2, mark3):
    """
    This function computes the joint angles for a given participant, trial and set of markers
    
    fw: a string that defines the footwear being studied; Should be either 'AFO', 'PPAFO' or 'Shoes'
    pnum: integer value for the participant number; Should be a number between 1 and 16
    trial: integer value for the trial number being studied; Should be a number between 1 and 10
    mark1: a string that defines the marker label for the marker above the joint being studied
    mark2: a string that defines the marker label for the marker at the joint being studied
    mark3: a string that defines the marker label for the marker below the joint being studied
    
    returns indices (a list of frame numbers), theta_t (a list of joint angles in radians)
    """
    
    theta_t=[]
    
    if fw=='AFO':
        dset=AFO
        
    if fw=='PPAFO':
        dset=PPAFO
        
    if fw=='Shoes':
        dset=Shoes
        
        
    MT_Obj=dset[pnum].GetTrial(trial) #AFO trial 4 for participant 1

    R_Lat_Knee_x = MT_Obj.x[mark1]
    R_Tib_x = MT_Obj.x[mark2]
    R_Thigh_x = MT_Obj.x[mark3]

    R_Lat_Knee_y = MT_Obj.y[mark1]
    R_Tib_y = MT_Obj.y[mark2]
    R_Thigh_y = MT_Obj.y[mark3]

    R_Lat_Knee_z = MT_Obj.z[mark1]
    R_Tib_z = MT_Obj.z[mark2]
    R_Thigh_z = MT_Obj.z[mark3]

#    x_dir_vec=[1,0,0]
#    y_dir_vec=[0,1,0]
#    z_dir_vec=[0,0,1]

    for i in range(len(R_Lat_Knee_x)):
    
        KneeTib_x=R_Lat_Knee_x[i]-R_Tib_x[i]
        KneeTib_y=R_Lat_Knee_y[i]-R_Tib_y[i]
        KneeTib_z=R_Lat_Knee_z[i]-R_Tib_z[i]
        
        ThighKnee_x=R_Lat_Knee_x[i]-R_Thigh_x[i]
        ThighKnee_y=R_Lat_Knee_y[i]-R_Thigh_y[i]
        ThighKnee_z=R_Lat_Knee_z[i]-R_Thigh_z[i]
    
        vec=[KneeTib_x, KneeTib_y, KneeTib_z]
        vec2=[ThighKnee_x, ThighKnee_y, ThighKnee_z]
    
        #Apply cos (theta) = (A dot B)/(modA modB)
        theta=math.acos((np.dot(vec, vec2))/((np.linalg.norm(vec))*(np.linalg.norm(vec2))))
    
        theta_t.append(theta/math.pi*180)
    
    indices=MT_Obj.x.index.get_values()
    
    return indices, theta_t
    #thinkplot.Show(legend=False)
    
############################################

def AngleDiff(AFO, PPAFO, Shoes, fw, participant, baselineTrial, WalkTrial, mark1, mark2, mark3, plot=False, reverse=False):
    """
    This function computes the difference between each angle in the walking trial and the median of the baseline trial to
    obtain the change in angle from baseline while the participant is walking.
    
    fw: a string that defines the footwear being studied; Should be either 'AFO', 'PPAFO' or 'Shoes'
    participant: integer value for the participant number; Should be a number between 1 and 16
    WalkTrial: integer value for the trial number of the walking trial being studied; Should be a number between 4 and 10
    mark1: a string that defines the marker label for the marker above the joint being studied
    mark2: a string that defines the marker label for the marker at the joint being studied
    mark3: a string that defines the marker label for the marker below the joint being studied
    
    returns R_angle_changes (list of change in joint angle from baseline in degrees)
    """

    #trial=3

    R_ind_base, R_theta_base=JointAngles(AFO, PPAFO, Shoes, fw, participant, baselineTrial, mark1, mark2, mark3)
    
    cdf1=thinkstats2.Cdf(R_theta_base)
    median_R=cdf1.Percentile(50)
    #print "Baseline Median =", median_R
    
    #trial=WalkTrial
    R_ind, R_theta=JointAngles(AFO, PPAFO, Shoes, fw, participant, WalkTrial, mark1, mark2, mark3)
    
    if plot==True:
        
        thinkplot.Cdf(cdf1)
        thinkplot.Show(legend=False, title='Angle Baseline', xlabel='Angle in degrees', ylabel='CDF')
        thinkplot.Plot(R_ind_base, R_theta_base)
        #thinkplot.Config(ylim=[135,145])
        thinkplot.Show(legend=False, title='Angle Baseline Time Series', xlabel='Time in frames', ylabel='Angle in degrees')

    
        cdf3=thinkstats2.Cdf(R_theta)
        thinkplot.Cdf(cdf3)
        thinkplot.Show(legend=False, title='Walking', xlabel='Angle in degrees', ylabel='CDF')
        thinkplot.Plot(R_ind, R_theta)
        #thinkplot.Config(ylim=[135,145])
        thinkplot.Show(legend=False, title='Walking Time Series', xlabel='Time in frames', ylabel='Angle in degrees')

    R_angle_changes=[]

    if reverse==True:
        for eachang in R_theta:
            R_angle_changes.append(-(eachang-median_R))
    elif reverse==False:
        for eachang in R_theta:
            R_angle_changes.append((eachang-median_R))
        
        
    return R_angle_changes

##########################################
def RemoveNans(L_angle, R_angle):
    """
    This function takes two sequences and removes the nans from each of them independently (i.e. there is 
    no dependence on both sequences when removing nans)
    
    L_angle: Sequence of data for left leg
    R_angle: sequence of data for right leg
    
    returns a tuple containinclean_L, clean_R
    """
    clean_L=[]
    clean_R=[]
    
    for i in range(len(L_angle)):
        if np.isnan(L_angle[i]) != True:
            clean_L.append(L_angle[i])
    
    for j in range(len(R_angle)):        
        if np.isnan(R_angle[j]) != True:
            clean_R.append(R_angle[j])
            
    return clean_L, clean_R