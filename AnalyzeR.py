"""
File: ReadCsvs.py
Created on Sat Feb  7 23:57:02 2015

Code authored by Justin Poh for Data Science, Spring 2015

This module is used to compute SD and mean for the residual provided in the dataset
"""

import thinkstats2
import ReadCsvs as rc

data=rc.ReadGaitData()

t=[data.afo, data.ppafo, data.shoes]

for fw in t:
    for dataset in fw.keys():
        R_df=fw[dataset].r
        markers=R_df.columns
        for marker in markers:
            R_Val=R_df[marker]
            hist=thinkstats2.Hist(R_Val)
            print hist.mean