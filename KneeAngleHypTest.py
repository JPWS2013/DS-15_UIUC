# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 21:41:03 2015

@author: jpoh
"""
import thinkstats2
import numpy as np
import JointAngFuncs as jaf

class KneeAngleHT(thinkstats2.HypothesisTest):
    """
    Defines the knee angle hypothesis test class that inherits from the hypothesis test class from thinkstats2
    
    """
    
    def TestStatistic(self, data):
        """
        Defines the test statistic method required by the hypothesis test parent class
        In this implementation, it simply computes the difference between means
        
        data: tuple of two sequences, one for each of the two groups being compared
        
        returns: the difference between the means for the two groups (i.e. group1mean - group2mean)
        """
        
        raw_group1, raw_group2 = data
        
        group1=np.asarray(raw_group1)
        group2=np.asarray(raw_group2)
        
        test_stat=group1.mean()-group2.mean()
        #print "test_stat=", test_stat
        return test_stat
    
    def MakeModel(self):
        """
        Defines the MakeModel method required by the hypothesis test parent class
        In this implementation, it simply stacks the data for each of the two groups, one on top of the other
        
        Does not return anything; Adds the stacked data to the pool attribute
        """
        
        group1, group2 = self.data
        self.n, self.m=len(group1), len(group2)
        self.pool=np.hstack((group1, group2))
        
        #print "group1len=", len(group1)
        #print "group2len=",len(group2)
        #print "poollen=",len(self.pool)
        
    def RunModel(self):
        np.random.shuffle(self.pool)
        data=self.pool[:self.n], self.pool[self.n:]
        return data
        

def KneeAngleHypTest(Raw_data1, Raw_data2):
    """
    This function carries out the knee angle hypothesis test and returns the pvalue
    
    Raw_data1: Sequence of data for group 1
    Raw_data2: Sequence of data for group 2
    
    returns: pvalue of the hypothesis test
    """
    
    data1, data2=jaf.RemoveNans(Raw_data1, Raw_data2)

    #test=np.asarray(PPAFO_angle).mean()-np.asarray(AFO_angle).mean()
        
    #print "test=", test
    #print np.asarray(data1).mean()
    #print np.asarray(data2).mean()

    #print AFO_angle
    data=(data1, data2)
    ht=KneeAngleHT(data)
    print "Actual Observed Effect Size=", ht.actual

    pvalue=ht.PValue()

    return pvalue
    
def KneeAngleHypTest_General(AFO, PPAFO, Shoes, fw1, fw2, pnum, baselinetrial, trialnum, side):
    """
    This function is the generalized version of the KneeAngleHypTest that carries out the knee angle hypothesis test and returns the pvalue
    
    AFO: Data Dictionary for the AFO condition
    PPAFO: Data Dictionary for the PPAFO condition
    Shoes: Data Dictionary for the Shoes condition
    fw1: string specifying footwear condition 1
    fw2: string specifying footwear condition 2
    pnum: integer for participant number
    baselinetrial: integer specifying the trial number for the baseline
    trialnum: integer specifying the trial number for the walking trial
    
    returns: pvalue of the hypothesis test
    """
    if side=='R':
        mark1='R_TROCH'
        mark2='R_LAT_KNEE'
        mark3='R_LAT_MAL'
    
    if side == 'L':
        mark1='L_TROCH'
        mark2='L_LAT_KNEE'
        mark3='L_LAT_MAL'
    
    Raw_data1=jaf.AngleDiff(AFO, PPAFO, Shoes, fw1, pnum, baselinetrial, trialnum, mark1, mark2, mark3, False, False)
    Raw_data2=jaf.AngleDiff(AFO, PPAFO, Shoes, fw2, pnum, baselinetrial, trialnum, mark1, mark2, mark3, False, False)
    
    data1, data2=jaf.RemoveNans(Raw_data1, Raw_data2)
    
    testmean_1=np.asarray(data1).mean()
    testmean_2=np.asarray(data2).mean()
    
    print testmean_1
    print testmean_2
    
    if np.isnan(testmean_1)!=True and np.isnan(testmean_2)!=True:
        #print AFO_angle
        data=(data1, data2)
        ht=KneeAngleHT(data)
        print "Actual Observed Effect Size=", ht.actual

        pvalue=ht.PValue()
        return (pvalue, ht.actual)
    else:
        print "Participant ", pnum, "Trial ", trialnum, "has returned nan so it will be skipped!"