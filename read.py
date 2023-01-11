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
import pandas as pd
import pickle
import dill
import functions

# define variables --------------------------------------------------------------------------------------------------
datapath        = os.getcwd() + "\\data\\Experiment\\"        # full path to read recorded data
savepath        = os.getcwd() + "\\save\\"        # full path to save calculated data

exp_header      = [ "f", "dt", "t", "fps", "start", "hand", "Grip", "Tracked", "Controlling" ]
gaze_header     = [ "f", "dt", "t", "status", "gazeX", "gazeY", "gazeZ", "gazeposition", "focusdistance", "focusstability", "statusL", "LeftX", "LeftY", "LeftZ", "posL", "pupilL", "statusR", "RightX", "RightY", "RightZ", "positionR", "pupilR"]
hand_header     = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grab", "pinch", "CMDposX", "CMDPosY", "CMDposZ", "CMDrotX", "CMDrotY", "CMDrotZ", "CMDrotW"]
hmd_header      = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotw"]
gripper_header  = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grip_pos", "grip_vel", "grip_eff" ]
robot_header    = [ "f", "dt", "t", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "fx", "fy", "fz" ]

Participants    = [1, 2, 3, 4, 5, 6, 7, 8, 9]                            # number of participants
Conditions      = ['A', 'B', 'C', 'D', 'E', 'F']
Trials          = [1, 2, 3]
Files           = ['Experiment', 'Gaze', 'Hand', 'HMD', 'Gripper', 'Robot']
Headers         = [exp_header, gaze_header, hand_header, hmd_header, gripper_header, robot_header]

data = {Participant: {Condition: {Trial: {File: {} for File in Files} for Trial in Trials} for Condition in Conditions} for Participant in Participants}

#%% Read data ----------------------------------------------------------------------------------------------------------------------
for p in Participants: 
    print(), print(), print('Reading data for participant {}'.format(p))    
    
    for c in Conditions[1:]:        
        print(), print('Condition {}'.format(c))

        for t in Trials:           
            for f,h in zip(Files, Headers):
                data[p][c][t].update({f: functions.read_csv(datapath, p, c, t, f + '.csv', h)})
            
#%% save imported data
print(), print('Dumping raw data to file...')
dill.dump_session('data_raw.pkl')

# %%
