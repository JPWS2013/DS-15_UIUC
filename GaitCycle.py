
"""
File: GaitCycle.py
Created on Sat Feb 12 2:58:02 2015

Code authored by Julianne Jorgensen for Data Science, Spring 2015

This module takes the spaciotemporal data and converts it to gait cycles based on the left heel.
"""

""" Fourier transform of the data to get the frequency"""
#import
import numpy as np
import ReadCsvs as rc

#data
data=rc.ReadGaitData()
t=[data.afo, data.ppafo, data.shoes]
dft_x = []
dft_y = []
dft_z = []

#DFT - transform of gait
for value in t:
        for dataset in value.keys():
            X_df=value[dataset].x
            Y_df=value[dataset].y
            Z_df=value[dataset].Z
            markers_x=X_df.columns
            markers_y=Y_df.columns
            markers_z=Z_df.columns
            for marker in markers_x:
                dft_x += np.fft(marker)
            for marker in markers_y:
                dft_y += np.fft(marker)
            for marker in markers_z:
                dft_z += np.fft(marker)
