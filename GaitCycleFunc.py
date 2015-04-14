# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 11:48:55 2015

@author: jpoh
"""
import numpy as np
import pylab as plt
import thinkstats2
import thinkplot

def FreqCalc(data, sel_marker, pnum, trialnum, fwchoice):

#FullLabelSet=['SACRAL', 'R_ASIS', 'R_TROCH', 'R_THIGH', 'R_LAT_KNEE', 'R_TIB', 'R_LAT_MAL', 'R_TOE_5', 'R_TOE_1', 'R_MED_MAL', 'R_HEEL', 'R_MED_KNEE', 'L_MED_KNEE', 'L_HEEL', 'L_MED_MAL', 'L_TOE_1', 'L_TOE_5', 'L_LAT_MAL', 'L_TIB', 'L_LAT_KNEE', 'L_TROCH', 'L_THIGH', 'L_ASIS']
#Left = ['L_MED_KNEE', 'L_HEEL', 'L_MED_MAL', 'L_TOE_1', 'L_TOE_5', 'L_LAT_MAL', 'L_TIB', 'L_LAT_KNEE', 'L_TROCH', 'L_THIGH', 'L_ASIS']
#Right = ['R_ASIS', 'R_TROCH', 'R_THIGH', 'R_LAT_KNEE', 'R_TIB', 'R_LAT_MAL', 'R_TOE_5', 'R_TOE_1', 'R_MED_MAL', 'R_HEEL', 'R_MED_KNEE']
#j = 1 #subject number
#i = 3 #trial number

    if fwchoice=='AFO':
        choicedata=data[0]
    elif fwchoice=='PPAFO':
        choicedata=data[1]
    elif fwchoice=='Shoes':
        choicedata=data[2]
    
    frames = choicedata[pnum].trials[trialnum].frames
    framerate = choicedata[pnum].trials[trialnum].framerate
    drop_NA = []
    
    #Assign a time from frame and frame  - in seconds
    choicedata[pnum].trials[trialnum].x["times"] = np.arange(0, frames) * (1.0/framerate)
    #times = choicedata[pnum].trials[trialnum].x["times"]

    vel_t = []
    acc_t = []
    marker_t = []
    time_t = []   
    
    for label in sel_marker:
        #drop NA from times and marker values
        drop_NA = choicedata[pnum].trials[trialnum].x[["times", label]]
        drop_NA = drop_NA.dropna()
        marker = drop_NA[label]
        marker_t.append(marker)
        if len(marker) == 0:
            continue
        time = drop_NA["times"]
        time_t.append(time) #Adds the time series to a master list
        timeshape = time.shape[0]
    
        #Computes velocity
        time_step = np.diff(time)
        velocity = np.diff(marker)/time_step
        vel_t.append(velocity) #Stores velocity to a master list

        #Computes acceleration
        vel_time_step = np.diff(time)
        acc = np.diff(velocity)/vel_time_step[:-1]
        acc_t.append(acc)
        #acc = AFO[j].trials[i].x["acc"]
        #drop_acc_NA = acc.dropna(subset=[['acc', 'time']])
        
        #DFT position
        dft = np.fft.fft(marker)
        freq = np.fft.fftfreq(timeshape)*framerate
        
        #DFT velocity
        dft_vel = np.fft.fft(velocity)
        time_stepshape = time_step.shape[0]
        freq_vel = np.fft.fftfreq(time_stepshape)*framerate
        
        #DFT acceleration
        dft_acc = np.fft.fft(acc)
        acc_timeshape = vel_time_step[:-1].shape[0]
        freq_acc = np.fft.fftfreq(acc_timeshape)*framerate 
    
        #plotting
#         plt.figure(0)
#         plt.title("Frequency of Right Marker Positions")
#         plt.plot(freq, 2.0/frames * np.abs(dft[0:frames]))
#         plt.xlim((0,15))
#         plt.xlabel("Frequency (Hz)")
#         plt.ylabel("DFT of %s Marker Positions" %label)
        
        v_time = time[:-1]
        print np.shape(v_time), np.shape(vel_t), np.shape(velocity)
#         plt.figure(1)
#         plt.plot(v_time, velocity)
#         plt.xlabel("Time(s)")
#         plt.ylabel("Velocity (mm/s)")
        
        plt.figure(0)
        plt.title("Frequency of Right Marker Frequencies")
        plt.plot(freq_vel, 2.0/frames * np.abs(dft_vel[0:frames]))
        plt.xlim((0,15))
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("DFT of %s Marker Velocities" %label)
    
        plt.figure(1)
        plt.plot(freq_acc, 2.0/frames * np.abs(dft_acc[0:frames]))
        plt.xlim((0,15))
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("DFT of %s Marker Accelerations" %label)
        
        plt.figure(2)
        plt.plot(time, marker, "o", alpha = .2)
        plt.xlabel("time (s)")
        plt.ylabel("Position of %s (mm)" %label)    
#         plt.figure()
#         plt.plot(time, marker, "o", alpha = .2)
#         plt.xlabel("time (s)")
#         plt.ylabel("Position of %s (mm)" %label)
        
        return time_t, vel_t, marker_t, dft, freq



def HeelStrike(fw, data, pnum, trial, mark1, mark2):
    """
    finding the initial heel strike
    """
    
    if fw=='AFO':
        dset=data[0]
    if fw=='PPAFO':
        dset=data[1]
    if fw=='Shoes':
        dset=data[2]
        
    MT_Obj = dset[pnum].GetTrial(trial) #AFO trial 4 for participant 1
    
    #R_Heel_x = MT_Obj.x[mark2]
    #R_Heel_y = MT_Obj.y[mark2]
    R_Heel_z = MT_Obj.z[mark2]
    #L_Heel_x = MT_Obj.x[mark1]
    #L_Heel_y = MT_Obj.y[mark1]
    #L_Heel_z = MT_Obj.z[mark1]
    
    #time and velocity calculations
    frames = MT_Obj.frames
    framerate = MT_Obj.framerate
    MT_Obj.z['time'] = np.arange(0, frames) * (1.0/framerate)
    time = MT_Obj.z['time']
    R_Heel_z = thinkstats2.Smooth(R_Heel_z, sigma=7)
    
    #velocity
    time_step = np.diff(time)
    velocity = np.diff(R_Heel_z)/time_step
    v_smooth = thinkstats2.Smooth(velocity)
    v_time = time[:-1]
    
    #acceleration
    a_time = v_time[:-1]
    #vel_time_step = np.diff(time)
    acc = np.diff(v_smooth)/a_time
    a_smooth = thinkstats2.Smooth(acc)
    
    pos = R_Heel_z[1:-1]
    vel = v_smooth[1:]
    acc = a_smooth
    heel = -15 * pos + -.1 * vel * vel +  .8 * acc
    
    filter = np.array([-1., -1., -1, -1, -1, -1, -1, -1,
                       0.,   0.,  0., 0., 0., 0,  0, 0])
    
    from scipy.signal import convolve
    down = convolve(vel, filter, 'same')
    
    heel += down*1.9
        
    #take derivative of heel
    down_time_step = np.diff(a_time)
    Max_zero = np.diff(down)/down_time_step
    
    #find maxima of derivative of heel
    threshold = 2000
    maxima = []
    index = []
    strike_time = []
    heel_strike = []
    
    for i in range(len(Max_zero) - 1):
        if Max_zero[i] > 0 and Max_zero[i+1] < 0 and down[i] > threshold:
            if (down[i+1] > down[i]):
                maxima.append([i+1, down[i+1]])
                index.append([i+1])
                strike_time.append(a_time[i+40])
                heel_strike.append(R_Heel_z[i+40])
            else:
                maxima.append([i, down[i]])
                index.append([i])
                strike_time.append(a_time[i+50])
                heel_strike.append(R_Heel_z[i+50])
    print maxima, strike_time, heel_strike

    plt.figure()
    plt.title("Convovled")
    plt.plot(a_time, down)   
    plt.xlabel("Time(s)")
    plt.ylabel("Convolved values")

    #plot against a_time, down and time, pos
#     plt.figure()
#     plt.title("heel strike")
#     plt.plot(time,R_Heel_z)
#     plt.plot(strike_time, heel_strike, 'o')
#     plt.xlabel("Time(s)")
#     plt.ylabel("Position (mm)")
    
#     plt.figure()
#     plt.title("Velocity")
#     plt.plot(v_time, v_smooth)
#     plt.xlabel("Time(s)")
#     plt.ylabel("Velocity(mm/s)")
    
#     plt.figure()
#     plt.title("Position")
#     plt.plot(time, R_Heel_z)
#     plt.xlabel("Time(s)")
#     plt.ylabel("Position (mm)")
    
    #down_dev = np.diff(down)/a_time[:-1]
    #mask = np.where(np.logical_and(down_dev>-10, down_dev<10))
    #a_mask = np.where(acc<0)
    #plt.figure(5)
    #plt.plot(a_time[:-1],down_dev, 'o')
   
#     plt.title("heel val")
#     plt.plot(a_time, heel)
#     plt.ylim([-10000, 4000])
    
    #vel_zero = R_Heel_z[np.where(np.logical_and(velocity>-5, velocity<5))]
    #acc_neg = R_Heel_z[np.where(acc<0)]
    #v_mask = np.where(np.logical_and(velocity>-5, velocity<5))
    #a_mask = np.where(acc<0)
    return heel_strike, time, R_Heel_z, v_time, vel, a_time, down, heel

def EstimatedAutocorr(x):
    """
    Using autocorrelation transpose the signal until the two signals line up. The first heel strike should overlay the second.
    """   
    x = cycle_start[2]
    time = cycle_start[1]
    drop_NA = np.vstack((x[:-1], time))
    #print drop_NA.shape, x.shape, y.shape
    drop_NA = drop_NA.T
    x = drop_NA[0]
    x = x[~np.isnan(x).any()]
 
    #n = len(x)
    #var = np.var(x)
    tao = np.correlate(x, x, mode='full')
    # assert np.allclose(r, np.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    #result = r/(var*(np.arange(n, 0, -1)))
    plt.figure(4)
    plt.plot(tao)
    return tao

if __name__ == '__main__':
    import ReadCsvs as rc
    
    data=rc.ReadGaitData()
    
    AFO_cycle_start = [HeelStrike('AFO', data, x, 4, 'L_HEEL', 'R_HEEL') for x in [1, 2, 4]]
    PPAFO_cycle_start = [HeelStrike('PPAFO', data, x, 4, 'L_HEEL', 'R_HEEL') for x in [1, 2, 4]]
    Shoes_cycle_start = [HeelStrike('Shoes', data, x, 4, 'L_HEEL', 'R_HEEL') for x in [1, 2, 4]]
    