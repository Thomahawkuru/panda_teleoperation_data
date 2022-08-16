# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import os
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import readers
import calculators

#%% define variables --------------------------------------------------------------------------------------------------
datapath        = os.getcwd() + "/data/"        # full path to read recorded data
savepath        = os.getcwd() + "/save/"        # full path to save calculated data
participants    = 22                            # number of participants

columns_R       = ['RPos_X', 'RPos_Y', 'RPos_Z']
columns_L       = ['LPos_X', 'LPos_Y', 'LPos_Z']

exp_header      = [ "f", "dt", "t", "start", "grip" ];
gaze_header     = [ "f", "dt", "t", "status", "GazeX", "GazeY", "GazeZ", "GazePosition", "FocusDistance", "FocusStability", "StatusL", "LeftX", "LeftY", "LeftZ", "PositionL", "PupilL", "StatusR", "RightX", "RightY", "RightZ", "PositionR", "PupilR"];
hand_header     = [ "f", "dt", "t", "LPos_X", "LPos_Y", "LPos_Z", "LRot_X", "LRot_Y", "LRot_Z", "LRot_W", "LGrab", "LPinch", "RPos_X", "RPos_Y", "RPos_Z", "RRot_X", "RRot_Y", "RRot_Z", "RRot_W", "RGrab", "RPinch" ];
hmd_header      = [ "f", "dt", "t", "Pos_X", "Pos_Y", "Pos_Z", "Rot_X", "Rot_Y", "Rot_Z"];
panda_header    = [ "f", "dt", "t", "Pos_X", "Pos_Y", "Pos_Z", "Rot_X", "Rot_Y", "Rot_Z", "Rot_W", "Gripper" ];
    

#%% Import data --------------------------------------------------------------------------------------------------
exp_data         = {}
gaze_data        = {}
hand_data        = {}
hmd_data         = {}
panda_data       = {}
completion_times = {}
handedness       = {}

for p in range(1, participants + 1):
    print(), print(), print('Reading data for participant {}'.format(p))    
    
    exp_data[p]           = readers.csv(datapath, p, 'Experiment.csv', exp_header)
    gaze_data[p]          = readers.csv(datapath, p, 'Gaze.csv', gaze_header)
    hand_data[p]          = readers.csv(datapath, p, 'Hand.csv', hand_header)
    hmd_data[p]           = readers.csv(datapath, p, 'HMD.csv', hmd_header)
    panda_data[p]         = readers.csv(datapath, p, 'Panda.csv' , panda_header)
    
    completion_times[p]   = readers.times(datapath, p)
    handedness[p]         = readers.handedness(datapath,p)
    
#%%plot data
data = np.array(list(completion_times.items()))
fig1 = ff.create_distplot([data[:,1]], ['completion times [s]'])
plot(fig1)

#%% Velocity
input_velocity = {}

for p in range(1, participants + 1):
    if handedness[p] == 'R':
        input_velocity[p] = calculators.velocity(hand_data[p], columns_R)
    elif handedness[p] == 'L':
        input_velocity[p] = calculators.velocity(hand_data[p], columns_L)
    
#%% plot data
fig1 = go.Figure()

for p in range(1, participants + 1):
   fig1.add_trace(go.Scatter(x=hand_data[p].t, y=input_velocity[p], name=str(p), mode="lines"))
    
plot(fig1)
    
    
#plt.plot(hand_data[1].LPos_X, hand_data[1].LPos_Z) 
#fig2 = px.line_3d(hand_data[1], x='LPos_Z', y='LPos_X', z='LPos_Y', title = 'Hand input')
#plot(fig2)
#input_paths         = calcualtors.input_paths(timestamps, hand_data)