# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import os
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import numpy as np
import readers
import calculators

#%% define variables --------------------------------------------------------------------------------------------------
datapath        = os.getcwd() + "/data/"        # full path to read recorded data
savepath        = os.getcwd() + "/save/"        # full path to save calculated data
participants    = 22                            # number of participants

experiment_header   = [ "f", "dt", "t", "start", "grip" ];
gaze_header         = [ "f", "dt", "t", "status", "GazeX", "GazeY", "GazeZ", "GazePosition", "FocusDistance", "FocusStability", "StatusL", "LeftX", "LeftY", "LeftZ", "PositionL", "PupilL", "StatusR", "RightX", "RightY", "RightZ", "PositionR", "PupilR"];
hand_header         = [ "f", "dt", "t", "LPos_X", "LPos_Y", "LPos_Z", "LRot_X", "LRot_Y", "LRot_Z", "LRot_W", "LGrab", "LPinch", "RPos_X", "RPos_Y", "RPos_Z", "RRot_X", "RRot_Y", "RRot_Z", "RRot_W", "RGrab", "RPinch" ];
hmd_header          = [ "f", "dt", "t", "Pos_X", "Pos_Y", "Pos_Z", "Rot_X", "Rot_Y", "Rot_Z"];
panda_header        = [ "f", "dt", "t", "Pos_X", "Pos_Y", "Pos_Z", "Rot_X", "Rot_Y", "Rot_Z", "Rot_W", "Gripper" ];
    
#%% Import data --------------------------------------------------------------------------------------------------
experiment_data = {}
gaze_data       = {}
hand_data       = {}
hmd_data        = {}
panda_data      = {}
completion_times= {}
handedness      = {}

for participant in range(1, participants + 1):
    print(), print(), print('Reading data for participant {}'.format(participant))    
    
    experiment_data[participant]    = readers.csv(datapath, participant, 'Experiment.csv', experiment_header)
    gaze_data[participant]          = readers.csv(datapath, participant, 'Gaze.csv', gaze_header)
    hand_data[participant]          = readers.csv(datapath, participant, 'Hand.csv', hand_header)
    hmd_data[participant]           = readers.csv(datapath, participant, 'HMD.csv', hmd_header)
    panda_data[participant]         = readers.csv(datapath, participant, 'Panda.csv' , panda_header)
    
    completion_times[participant]   = readers.times(datapath, participant)
    handedness[participant]         = readers.handedness(datapath,participant)
    
#%% plot data

#plt.plot(hand_data[1].t,hand_data[1].LPos_X)  
#plt.plot(hand_data[1].LPos_X, hand_data[1].LPos_Z) 
fig = px.line_3d(hmd_data[2], x='Pos_Z', y='Pos_X', z='Pos_Y', title = 'Hand input')
plot(fig)
#input_paths         = calcualtors.input_paths(timestamps, hand_data)