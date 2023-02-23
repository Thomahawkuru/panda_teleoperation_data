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
import math

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

    # plt.plot(grab_crop)
    # plt.plot(peaks_succes,grab_crop[peaks_succes],'bx')
    # plt.plot(startpoints,grab_crop[startpoints],'gx')
    # plt.plot(endpoints,grab_crop[endpoints],'rx')
    # plt.show()

    grabs['succes'] = len(peaks_succes)
    grabs['fail'] = len(peaks_fail)
    grabs['attempts'] = grabs['succes'] + grabs['fail']

    return grabs

def grab_velocity(data, p, c, t, file, pre_time):
    avg_v = {'pre': [], 'post': []}

    grab_data = -data[p][c][t]['Gripper']["grip_pos"]
    input_data = data[p][c][t][file][["dt", "posX", "posY", "posZ"]]   
    grab_crop = grab_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)
    input_crop = input_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)

    peaks_succes, _ = signal.find_peaks(grab_crop, height = [-0.035, -0.02], prominence=0.005, distance=50)
    startpoints, endpoints = functions.grab_start_end(grab_crop, peaks_succes)        
    prepoints = functions.pre_grap_location(input_data, startpoints, pre_time)

    post_grab_v = []
    pre_grab_v = []
    
    for g in range(len(startpoints)):
        pre_grab_input = input_crop.loc[prepoints[g]:startpoints[g]]
        pre_dist = math.dist(pre_grab_input.iloc[0,[1,2,3]], pre_grab_input.iloc[-1,[1,2,3]])
        pre_time = np.sum(pre_grab_input.iloc[:,[0]])
        pre_grab_v.append(pre_dist/pre_time)

        post_grab_input = input_crop.loc[startpoints[g]:endpoints[g]]
        post_dist = math.dist(post_grab_input.iloc[0,[1,2,3]], post_grab_input.iloc[-1,[1,2,3]])
        post_time = np.sum(post_grab_input.iloc[:,[0]])
        post_grab_v.append(post_dist/post_time)

    avg_v['pre'] = np.mean(pre_grab_v)
    avg_v['post'] = np.mean(post_grab_v)

    # grab_start = input_crop.iloc[startpoints,[1,2,3]]
    # grab_end = input_crop.iloc[endpoints,[1,2,3]]
    # fig1 = px.line_3d(input_crop, x='posZ', y='posX', z='posY', title = 'Hand input')
    # fig2 = px.scatter_3d(grab_start, x='posZ', y='posX', z='posY',color_discrete_sequence=['green'])
    # fig3 = px.scatter_3d(grab_end, x='posZ', y='posX', z='posY',color_discrete_sequence=['red'])
    # fig4 = go.Figure(data=fig1.data + fig2.data + fig3.data)
    # plot(fig4, filename='plots/fig{}{}{}.html'.format(p,c,t))

    return avg_v

def input_depth(data, p, c, t):
    input_z = functions.crop_data(data[p][c][t]['Hand']['posZ'], data[p][c][t]['Experiment'])
    mean_z, std_z = functions.pdf(input_z)

    depth = std_z*6

    return depth