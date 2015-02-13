# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 05:11:07 2015

@author: jjorgensen
------
Python validation
"""

import thinkstats2
import thinkplot
import ReadCsvs as rc

data = rc.ReadGaitData()

for run in data:
    hist = thinkstats2.Hist(run)
    thinkplot.Hist(hist)
    thinkplot.Show
    
""" Compare these histograms to the ones output by MATLAB_valid"""    