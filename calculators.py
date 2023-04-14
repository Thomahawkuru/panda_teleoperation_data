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
from scipy.spatial.transform import Rotation
import functions
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import math

def fps(data, p, c, t, debug):
    fps = functions.crop_data(data[p][c][t]['Experiment'].fps, data[p][c][t]['Experiment'])
    avg_fps = np.mean(data[p][c][t]['Experiment'].fps)

    if debug is True:
        time = functions.crop_data(data[p][c][t]['Experiment']["t"], data[p][c][t]['Experiment'])-4
        fig, ax = plt.subplots()
        ax.plot(time, fps, label='raw FPS')
        ax.axhline(avg_fps, color='r', label='Average FPS')
        ax.set_title(f'FPS for participant {p}, condition {c}, trial {t}')
        ax.set_xlabel('time [s]'), ax.set_ylabel('FPS')
        ax.legend()
        plt.show()

    return avg_fps

def duration(data, p, c, t, debug):
    time_raw = data[p][c][t]['Experiment']["t"][data[p][c][t]['Experiment'].start]
    duration = np.max(time_raw - np.min(time_raw)) + data[p][c][t]['Experiment']["dt"][data[p][c][t]['Experiment'].start].tail(1)
   
    return float(duration)

def time(data, p, c, t, debug):
    time_raw = data[p][c][t]['Experiment']["t"]
    time_crop = functions.crop_data(data[p][c][t]['Experiment']["t"], data[p][c][t]['Experiment'])
    
    if debug is True:
        fig, ax = plt.subplots()
        ax.plot(time_raw, label='Total recording time')
        ax.plot(time_crop, label='Execution time')
        ax.set_title(f'Experiment time for participant {p}, condition {c}, trial {t}')
        ax.set_xlabel('datapoints [n]'), ax.set_ylabel('Time [s]')
        ax.legend()
        plt.show()

    return time_crop

def track_error(data, p, c, t, debug):
    checks = -data[p][c][t]['Experiment']["Controlling"][data[p][c][t]['Experiment'].start]
    peaks, _ = signal.find_peaks(checks)
    errors = len(peaks)

    if debug is True:
        peaks = checks.index[peaks] 
        time = data[p][c][t]['Experiment']["t"][data[p][c][t]['Experiment'].start]-4
        fig, ax = plt.subplots()
        ax.plot(time, checks, label='Tracking checks')
        ax.plot(time[peaks], checks[peaks],'rx', label='Detected tracking loss')
        ax.set_title(f'Tracking loss for participant {p}, condition {c}, trial {t}')
        ax.set_xlabel('time [s]'), ax.set_ylabel('Tracking loss check [True/False]')
        ax.legend()
        plt.show()

    return errors

def grabs(data, p, c, t, debug):
    grabs = {}
    grab_data = -data[p][c][t]['Gripper']["grip_pos"]
    grab_crop = grab_data.loc[data[p][c][t]['Experiment'].start].reset_index(drop = True)

    peaks_succes, _ = signal.find_peaks(grab_crop, height = [-0.035, -0.02], prominence=0.005, distance=50)
    peaks_fail, _   = signal.find_peaks(grab_crop, height = -0.02, prominence=0.005,distance=50)

    if debug is True:
        time = data[p][c][t]['Experiment']["t"][data[p][c][t]['Experiment'].start].reset_index(drop=True)-4
        fig, ax = plt.subplots(figsize=(7.5, 2.5))
        ax.plot(time,grab_crop, label='Grab width [m]')
        ax.plot(time[peaks_succes],grab_crop[peaks_succes],'gx', label='Succesful grabs')
        ax.plot(time[peaks_fail],grab_crop[peaks_fail],'rx', label='Failed grabs')
        ax.set_title(f'Grab identification for participant {p}, condition {c}, trial {t}', wrap=True)
        ax.set_xlabel('time [s]'), ax.set_ylabel('-Width [m]')
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        fig.tight_layout()
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

        fig1, ax1 = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(7.5, 5))
        ax1.plot(input_crop['posZ'], input_crop['posX'], input_crop['posY'], label='Hand input')
        ax1.plot(grab_start['posZ'], grab_start['posX'], grab_start['posY'], 'go', label='Startpoints')
        ax1.plot(grab_end['posZ'], grab_end['posX'], grab_end['posY'], 'ro', label='Endpoints')
        ax1.plot(grab_pre['posZ'], grab_pre['posX'], grab_pre['posY'], 'yo', label='Prepoints')
        ax1.set_title(f'Input path with grabpoints for participant {p}, conditon {c}, trial {t}')
        ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        fig1.tight_layout()

        fig2, ax2 = plt.subplots(figsize=(7.5,2.5))
        time = data[p][c][t]['Experiment']["t"][data[p][c][t]['Experiment'].start].reset_index(drop=True)-4

        ax2.plot(time, input_crop['grab'], label='Grab input')
        ax2.plot(time, grab_crop, label='Gripper width [m]')
        ax2.plot(time[peaks_succes],grab_crop[peaks_succes], 'bx', label='Succesfull grabs')
        ax2.plot(time[startpoints],input_crop['grab'][startpoints], 'gx', label='Startpoints')
        ax2.plot(time[endpoints],input_crop['grab'][endpoints], 'rx', label='Endpoints')
        ax2.plot(time[prepoints],input_crop['grab'][prepoints], 'yx', label='Preppoints')
        ax2.set_xlabel('Time [s]'), ax2.set_ylabel('Grabbing strenght [0-1]')
        ax2.set_title(f'Grabpoint detection for participant {p}, conditon {c}, trial {t}')
        ax2.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        fig2.tight_layout()

        plt.show()

    return avg_v

def head_movement(data, p, c, t, debug):
    HMD = functions.crop_data(data[p][c][t]['HMD'], data[p][c][t]['Experiment'])
    HMD = HMD.reset_index(drop=True)    
    u = []
    v = []
    w = []

    for i in range(len(HMD)):
        Q = HMD.loc[i, ['rotX', 'rotY', 'rotZ', 'rotw']].to_numpy()
        R = Rotation.from_quat(Q).as_matrix()
        direction = R @ np.array([1, 0, 0])
        u.append(direction[0])
        v.append(direction[1])
        w.append(direction[2])

    if debug is True:
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(7.5, 5))        
        ax.plot(HMD['posZ'], HMD['posX'], HMD['posY'], label='Position')
        ax.set_title(f'HMD movement for participant {p}, condition {c}, Trial {t}')
        for i in range(0, len(HMD), 20):
            ax.quiver(HMD['posZ'][i], HMD['posX'][i], HMD['posY'][i], u[i], v[i], w[i], color='red', length=0.01)
        ax.quiver(HMD['posZ'][i], HMD['posX'][i], HMD['posY'][i], u[i], v[i], w[i], color='red', length=0.01, label='Direction')
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        fig.tight_layout()
        plt.show()

    mean, pos = functions.pdf(HMD.iloc[:,3:6])
    pos_std = np.sqrt(sum(pos))

    mean, rot = functions.pdf(pd.DataFrame([u,v,w]).transpose())
    rot_std = np.sqrt(sum(rot))

    HMD_std ={'position': pos_std, 'rotation': rot_std} 

    return HMD_std

def in_out_corr(data, p, c, t, debug):
    input = functions.crop_data(data[p][c][t]['Hand'][["CMDposX", "CMDPosY", "CMDposZ"]], data[p][c][t]['Experiment'])
    output = functions.crop_data(data[p][c][t]['Gripper'][["posX", "posY", "posZ"]], data[p][c][t]['Experiment'])

    input.columns= ["posZ", "posX", "posY"]
    input['posY'] = input['posY'] + 0.1
    input = input.sort_index(axis=1)
    output.columns= ["posX", "posY", "posZ"]

    correlation = np.mean(input.corrwith(output,axis=0))

    lags = range(-50, 50)
    corr_coeffs_x = [np.correlate(input['posX'], np.roll(output['posX'], -k), mode='valid')[0] for k in lags]
    corr_coeffs_y = [np.correlate(input['posY'], np.roll(output['posY'], -k), mode='valid')[0] for k in lags]
    corr_coeffs_z = [np.correlate(input['posX'], np.roll(output['posZ'], -k), mode='valid')[0] for k in lags]
    corr = np.mean(np.array([corr_coeffs_x,corr_coeffs_y,corr_coeffs_z]),axis=0)
    
    max_corr = max(corr)
    max_lag = lags[np.where(corr==max_corr)[0][0]]
  
    in_out ={'corr': correlation, 'max_corr': max_corr, 'lag': max_lag} 
    
    if debug is True:
        time = functions.crop_data(data[p][c][t]['Experiment']["t"], data[p][c][t]['Experiment']).reset_index(drop=True)-4
        fig1, ax1 = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(7.5, 5))   
        ax1.plot(input["posX"], input["posY"], input["posZ"], label='Input')
        ax1.plot(output["posX"], output["posY"], output["posZ"], label='Output')
        ax1.set_title(f'Input and output in 3D for participant {p}, condition {c}, trial {t}', wrap=True)
        ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        fig1.tight_layout()

        fig2,ax2 = plt.subplots(figsize=(7.5,2.5))
        ax2.plot(time, input, label=['Input [x]', 'Input [y]', 'Input [z]'])
        ax2.plot(time, output, label=['Output [x]', 'Output [y]', 'Output [z]'])
        ax2.set_title(f'Input and output per axis for participant {p}, condition {c}, trial {t}', wrap=True)
        ax2.set_xlabel('Time [s]'), ax2.set_ylabel('Position [m]')
        ax2.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        fig2.tight_layout()
        plt.show()

    return in_out

def force(data, p, c, t, debug):
    forcexyz = functions.crop_data(data[p][c][t]['Robot'][["fx", "fy", "fz"]], data[p][c][t]['Experiment'])
    force = np.linalg.norm(forcexyz, axis=1)

    min_peak_height = 10 # [N] set minimum peak height
    min_peak_distance = 60 # [frames] set minimum peak distance

    # find peaks in the force data with specified height and minimum distance
    peaks, _ = signal.find_peaks(force, height=min_peak_height, distance=min_peak_distance)

    if debug:
        time = functions.crop_data(data[p][c][t]['Experiment']["t"], data[p][c][t]['Experiment']).reset_index(drop=True)-4
        input = functions.crop_data(data[p][c][t]['Hand'][["CMDposX", "CMDPosY", "CMDposZ"]], data[p][c][t]['Experiment'])
        input = input.reset_index(drop=True)

        fig, ax = plt.subplots(figsize=(7.5, 2.5))
        ax.plot(time, force, label='Euclidean EE-Force [N]')
        #ax.plot(time, input*30, label='Input position')
        ax.plot(time[peaks], force[peaks], "rx", label='Peak Force [N]')
        ax.set_xlabel('Time [S]'), ax.set_ylabel('Force [N]')
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        ax.set_title(f'Peak force detection for participant {p}, condition {c}, trial {t}', wrap=True)
        fig.tight_layout()
        plt.show()

    return np.mean(force[peaks])

def count_average(Count):
    count_avg = Count
    count_avg['avg'] = Count.groupby(['Participant Number', 'condition'])['blocks'].transform(np.mean)
    count_avg = count_avg.melt(id_vars=['Participant Number', 'condition'], value_vars=['avg'], \
                                    var_name ='measure', value_name='blocks')
    count_avg = count_avg.drop_duplicates()

    return count_avg