# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from scipy import stats
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

def grabs(data, p, c, t, debug):
    grabs = {}
    grab_data = -data[p][c][t]['Gripper']["grip_pos"]
    grab_crop = grab_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)

    peaks_succes, _ = signal.find_peaks(grab_crop, height = [-0.035, -0.02], prominence=0.005, distance=50)
    peaks_fail, _   = signal.find_peaks(grab_crop, height = -0.02, prominence=0.005,distance=50)

    if debug is True:
        plt.plot(grab_crop)
        plt.plot(peaks_succes,grab_crop[peaks_succes],'bx')
        plt.plot(startpoints,grab_crop[startpoints],'gx')
        plt.plot(endpoints,grab_crop[endpoints],'rx')
        plt.show()

    grabs['succes'] = len(peaks_succes)
    grabs['fail'] = len(peaks_fail)
    grabs['attempts'] = grabs['succes'] + grabs['fail']

    return grabs

def grab_velocity(data, p, c, t, file, pre_time, debug):
    avg_v = {'pre': [], 'post': []}

    grab_data = -data[p][c][t]['Gripper']["grip_pos"]
    input_data = data[p][c][t][file][["dt", "posX", "posY", "posZ"]]   
    input_data['grab'] = data[p][c][t]['Hand']["pinch"]
    grab_crop = grab_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)
    input_crop = input_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)

    peaks_succes, _ = signal.find_peaks(grab_crop, height = [-0.035, -0.02], prominence=0.005, distance=50)
    startpoints, endpoints = functions.grab_start_end(input_crop['grab'], peaks_succes)   
    prepoints = functions.pre_grap_location(input_data, startpoints, pre_time)
    
    if debug is True:
        plt.plot(input_crop['grab'])
        plt.plot(grab_crop)
        plt.plot(peaks_succes,grab_crop[peaks_succes],'bx')
        plt.plot(startpoints,input_crop['grab'][startpoints],'gx')
        plt.plot(endpoints,input_crop['grab'][endpoints],'rx')
        plt.plot(prepoints,input_crop['grab'][prepoints],'yx')
        plt.show()
    
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

    if debug is True:

        grab_pre = input_crop.iloc[prepoints,[1,2,3]]
        grab_start = input_crop.iloc[startpoints,[1,2,3]]
        grab_end = input_crop.iloc[endpoints,[1,2,3]]
        fig1 = px.line_3d(input_crop, x='posZ', y='posX', z='posY', title = 'Hand input')
        fig2 = px.scatter_3d(grab_start, x='posZ', y='posX', z='posY',color_discrete_sequence=['green'])
        fig3 = px.scatter_3d(grab_end, x='posZ', y='posX', z='posY',color_discrete_sequence=['red'])
        fig4 = px.scatter_3d(grab_pre, x='posZ', y='posX', z='posY',color_discrete_sequence=['yellow'])
        fig5 = go.Figure(data=fig1.data + fig2.data + fig3.data + fig4.data)
        plot(fig5, filename='plots/fig{}{}{}.html'.format(p,c,t))

    return avg_v

def input_depth(data, p, c, t):
    input_z = functions.crop_data(data[p][c][t]['Hand']['posZ'], data[p][c][t]['Experiment'])
    mean_z, std_z = functions.pdf(input_z)

    depth = std_z*6

    return depth

def head_movement(data, p, c, t, debug):
    HMD = functions.crop_data(data[p][c][t]['HMD'], data[p][c][t]['Experiment'])
    
    if debug is True:
        fig = px.line_3d(HMD, x='posZ', y='posX', z='posY', title = 'HMD_movement')
        fig.show()

    mean, std = functions.pdf(HMD.iloc[:,3:10])
    pos_std = np.sqrt(sum(std[:3]))
    rot_std = np.sqrt(sum(std[3:]))

    HMD_std ={'position': pos_std, 'rotation': rot_std} 

    return HMD_std

def in_out_corr(data, p, c, t, debug):
    input = functions.crop_data(data[p][c][t]['Hand'][["CMDposX", "CMDPosY", "CMDposZ"]], data[p][c][t]['Experiment'])
    output = functions.crop_data(data[p][c][t]['Gripper'][["posX", "posY", "posZ"]], data[p][c][t]['Experiment'])

    input.columns= ["posZ", "posX", "posY"]
    input['posY'] = input['posY'] + 0.1
    input = input.sort_index(axis=1)
    output.columns= ["posX", "posY", "posZ"]

    lags = range(-50, 50)
    corr_coeffs_x = [np.correlate(input['posX'], np.roll(output['posX'], -k), mode='valid')[0] for k in lags]
    corr_coeffs_y = [np.correlate(input['posY'], np.roll(output['posY'], -k), mode='valid')[0] for k in lags]
    corr_coeffs_z = [np.correlate(input['posX'], np.roll(output['posZ'], -k), mode='valid')[0] for k in lags]

    correlation = np.mean(input.corrwith(output,axis=0))
    corr = np.mean(np.array([corr_coeffs_x,corr_coeffs_y,corr_coeffs_z]),axis=0)/100
    max_corr = max(corr)
    max_lag = lags[np.where(corr==max_corr)[0][0]]

    # print('pearson correlation coefficient:', correlation)
    # print('Maximum correlation coefficient:', max_corr)
    # print('Lag at which maximum correlation occurs:', max_lag)
    
    in_out ={'corr': correlation, 'max_corr': max_corr, 'lag': max_lag} 
    
    if debug is True:
        plt.plot(input)
        plt.plot(output)
        plt.savefig('test.jpg')

    return in_out

def force(data, p, c, t, debug):
    forcexyz = functions.crop_data(data[p][c][t]['Robot'][["fx", "fy", "fz"]], data[p][c][t]['Experiment'])
    force = np.linalg.norm(forcexyz, axis=1)

    min_peak_height = 10 # [N] set minimum peak height
    min_peak_distance = 60 # [s] set minimum peak distance

    # find peaks in the force data with specified height and minimum distance
    peaks, _ = signal.find_peaks(force, height=min_peak_height, distance=min_peak_distance)

    if debug:
        input = functions.crop_data(data[p][c][t]['Hand'][["CMDposX", "CMDPosY", "CMDposZ"]], data[p][c][t]['Experiment'])
        input = input.reset_index(drop=True)
        plt.plot(force)
        plt.plot(input*30)

        # plot the force data and highlight the peaks
        plt.plot(force)
        plt.plot(peaks, force[peaks], "x")
        checks = -data[p][c][t]['Experiment']["Controlling"][data[p][c][t]['Experiment'].start]
        peaks, _ = signal.find_peaks(checks)
        plt.plot(checks.reset_index(drop=True))
        plt.plot(peaks, force[peaks], "rx")
        plt.show()

    return np.mean(force[peaks])