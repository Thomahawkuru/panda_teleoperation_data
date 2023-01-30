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
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go


def fps(data, p, c, t):
    fps = np.mean(data[p][c][t]['Experiment'].fps)

    return fps

def duration(data, p, c, t):
    time_raw = data[p][c][t]['Experiment']["t"][data[p][c][t]['Experiment'].start]
    duration = np.max(time_raw - np.min(time_raw)) + data[p][c][t]['Experiment']["dt"][data[p][c][t]['Experiment'].start].tail(1)

    
    return float(duration)

def time(data, p, c, t):
    time_crop = functions.crop_data(data[p][c][t]['Experiment']["t"], data[p][c][t]['Experiment'])
    
    return time_crop

def track_error(data, p, c, t):
    checks = -data[p][c][t]['Experiment']["Controlling"][data[p][c][t]['Experiment'].start]
    peaks, _ = signal.find_peaks(checks)

    errors = len(peaks)

    return errors

def grabs(data, p, c, t):
    grabs = {}
    grab_data = -data[p][c][t]['Gripper']["grip_pos"]
    grab_crop = grab_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)

    peaks_succes, _ = signal.find_peaks(grab_crop, height = [-0.035, -0.02], prominence=0.005, distance=50)
    peaks_fail, _   = signal.find_peaks(grab_crop, height = -0.02, prominence=0.005,distance=50)

    grabs['succes'] = len(peaks_succes)
    grabs['fail'] = len(peaks_fail)
    grabs['attempts'] = grabs['succes'] + grabs['fail']

    return grabs

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

def grab_velocity(data, p, c, t, file):

    grab_data = -data[p][c][t]['Gripper']["grip_pos"]
    input_data = data[p][c][t][file][["dt", "posX", "posY", "posZ"]]
    
    grab_crop = grab_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)
    input_crop = input_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)

    peaks_succes, _ = signal.find_peaks(grab_crop, height = [-0.035, -0.02], prominence=0.005, distance=50)

    peak = False
    startpoints = []
    endpoints = []
    
    for i in range(len(peaks_succes)):
        j = peaks_succes[i]

        while grab_crop[j] > -0.0395 and peak == False:
            j -= 1
            if grab_crop[j] < -0.0395:
                startpoints.append(j)    
                peak = True
                j += 1

        while grab_crop[j] > -0.0395 and peak == True:
            j += 1
            if j < len(grab_crop):
                if grab_crop[j] < -0.0395:                
                    endpoints.append(j)    
                    peak = False
            elif j == len(grab_crop):
                startpoints.remove(startpoints[-1])
                j -= 1
                peak = False
 
    # plt.plot(grab_crop)
    # plt.plot(peaks_succes,grab_crop[peaks_succes],'bx')
    # plt.plot(startpoints,grab_crop[startpoints],'gx')
    # plt.plot(endpoints,grab_crop[endpoints],'rx')
    # plt.show()

    # grab_start = input_crop.iloc[startpoints,[1,2,3]]
    # fig1 = px.line_3d(input_crop, x='posZ', y='posX', z='posY', title = 'Hand input')
    # fig1.update_traces(line=dict(color = 'rgba(100,0,0,0.5)'))
    # fig2 = px.scatter_3d(grab_start, x='posZ', y='posX', z='posY')
    # fig3 = go.Figure(data=fig1.data + fig2.data)
    # plot(fig3, filename='plots/fig{}{}{}.html'.format(p,c,t))

    v = [0.0]
    grab_v = [0.0]
    
    for g in range(len(startpoints)):

        data_3D = input_crop.loc[startpoints[g]:endpoints[g]]

        for i in range(1,len(data_3D.iloc[:, 0])):
            dx = data_3D.iloc[i,1]-data_3D.iloc[i-1,1]
            dy = data_3D.iloc[i,2]-data_3D.iloc[i-1,2]
            dz = data_3D.iloc[i,3]-data_3D.iloc[i-1,3]
            
            grab_v.append(np.sqrt(dx*dx + dy*dy + dz*dz)/data_3D.iloc[i,0])

        v.append(np.mean(grab_v))

    avg_v = np.mean(v)

    return avg_v

def input_depth(data, p, c, t):
    input_z = functions.crop_data(data[p][c][t]['Hand']['posZ'], data[p][c][t]['Experiment'])
    mean_z, std_z = functions.pdf(input_z)

    depth = std_z*6

    return depth