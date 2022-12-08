# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

#%% import
import os
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pickle
import dill
import readers
import calculators

#%% define variables --------------------------------------------------------------------------------------------------
datapath        = os.getcwd() + "\\data\\Experiment\\"        # full path to read recorded data
savepath        = os.getcwd() + "\\save\\"        # full path to save calculated data

exp_header      = [ "f", "dt", "t", "fps", "start", "hand", "Grip", "Tracked", "Controlling" ]
gaze_header     = [ "f", "dt", "t", "status", "gazeX", "gazeY", "gazeZ", "gazeposition", "focusdistance", "focusstability", "statusL", "LeftX", "LeftY", "LeftZ", "posL", "pupilL", "statusR", "RightX", "RightY", "RightZ", "positionR", "pupilR"]
hand_header     = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grab", "pinch", "CMDposX", "CMDPosY", "CMDposZ", "CMDrotX", "CMDrotY", "CMDrotZ", "CMDrotW"]
hmd_header      = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotw"]
gripper_header  = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grip_pos", "grip_vel", "grip_eff" ]
robot_header    = [ "f", "dt", "t", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "fx", "fy", "fz" ]

Participants    = [1,2]                            # number of participants
Conditions      = ['A', 'B', 'C', 'D', 'E', 'F']
Trials          = [1, 2, 3]
Files           = ['Experiment', 'Gaze', 'Hand', 'HMD', 'Gripper', 'Robot']
Headers         = [exp_header, gaze_header, hand_header, hmd_header, gripper_header, robot_header]

files = dict(zip(Files, [None]*len(Files)))
trials = dict(zip(Trials, [files]*len(Trials)))
conditions = dict(zip(Conditions, [trials]*len(Conditions))) 
data = dict(zip(Participants, [conditions]*len(Participants)))    

#%% Read data ----------------------------------------------------------------------------------------------------------------------
for p in Participants:
    exp_data         = {}
    gaze_data        = {}
    hand_data        = {}
    hmd_data         = {}
    gripper_data     = {}
    robot_data       = {}
    time             = {} 
    
    print(), print(), print('Reading data for participant {}'.format(p))    
    
    for c in Conditions:     
        
        print(), print('Condition {}'.format(c))
        if c == "A": 
            continue
        for t in Trials:    
            print('Trial {}'.format(t))
            for f,h in zip(Files, Headers):
                data[p][c][t][f] = readers.csv(datapath, p, c, t, f + '.csv', h)

#%% save imported data
dill.dump_session('data_raw.pkl')

# %%
