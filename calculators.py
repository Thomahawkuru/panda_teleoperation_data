# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
import functions

def fps(data, p, c, t):
    fps = np.mean(data[p][c][t]['Experiment'].fps)

    return fps

def duration(data, p, c, t):
    time_raw = data[p][c][t]['Experiment']["t"][data[p][c][t]['Experiment'].start]
    duration = np.max(time_raw - np.min(time_raw))

    return duration

def time(data, p, c, t):
    time_crop = functions.crop_data(data[p][c][t]['Experiment']["t"], data[p][c][t]['Experiment'])
    
    return time_crop

def velocity(data, p, c, t, file):
    v = [0.0]
    data_3D = data[p][c][t][file][["dt", "posX", "posY", "posZ"]]

    for i in range(1,len(data_3D.iloc[:, 0])):
        dx = data_3D.iloc[i,1]-data_3D.iloc[i-1,1]
        dy = data_3D.iloc[i,2]-data_3D.iloc[i-1,2]
        dz = data_3D.iloc[i,3]-data_3D.iloc[i-1,3]
        
        v.append(np.sqrt(dx*dx + dy*dy + dz*dz)/data_3D.iloc[i,0])
        
    velocity = functions.crop_data(pd.DataFrame(v), data[p][c][t]['Experiment']).to_numpy()

    return velocity

def grabs(data, p, c, t):
    grabs = {}
    grab_data = -data[p][c][t]['Gripper']["grip_pos"]
    grab_crop = grab_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)

    peaks_succes, _ = signal.find_peaks(grab_crop, height = [-0.035, -0.02], prominence=0.005, distance=50)
    peaks_fail, _   = signal.find_peaks(grab_crop, height = -0.02, prominence=0.005,distance=50)

    #plt.plot(grab_crop)
    #plt.plot(peaks_succes,grab_crop[peaks_succes],'gx')
    #plt.plot(peaks_fail, grab_crop[peaks_fail],'rx')
    #plt.show()

    grabs['succes'] = len(peaks_succes)
    grabs['fail'] = len(peaks_fail)

    return grabs