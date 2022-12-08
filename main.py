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
datapath        = os.getcwd() + "\\data\\Experiment\\"        # full path to read recorded data
savepath        = os.getcwd() + "\\save\\"        # full path to save calculated data

Participants    = [1]                            # number of participants
Conditions      = ['A', 'B', 'C', 'D', 'E', 'F']
Trials          = [1, 2, 3]
Files           = ['experiment', 'gaze', 'hand', 'hmd', 'gripper', 'robot']

columns_R       = ['RPos_X', 'RPos_Y', 'RPos_Z']
columns_L       = ['LPos_X', 'LPos_Y', 'LPos_Z']

exp_header      = [ "f", "dt", "t", "fps", "start", "hand", "Grip", "Tracked", "Controlling" ];
gaze_header     = [ "f", "dt", "t", "status", "gazeX", "gazeY", "gazeZ", "gazeposition", "focusdistance", "focusstability", "statusL", "LeftX", "LeftY", "LeftZ", "posL", "pupilL", "statusR", "RightX", "RightY", "RightZ", "positionR", "pupilR"];
hand_header     = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grab", "pinch", "CMDposX", "CMDPosY", "CMDposZ", "CMDrotX", "CMDrotY", "CMDrotZ", "CMDrotW"];
hand_hdr_short  = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grab", "pinch"];
hmd_header      = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ"];
gripper_header  = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grip_pos", "grip_vel", "grip_eff" ];
robot_header    = [ "f", "dt", "t", "tau1", "tau2", "tau3", "tau4", "tau5", "tau6", "tau7", "con_x", "con_y", "con_z" ];

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
            data[p][c][t]['experiment'] = readers.csv(datapath, p, c, t, 'Experiment.csv', exp_header)
            data[p][c][t]['gaze']       = readers.csv(datapath, p, c, t,'Gaze.csv', gaze_header)
            data[p][c][t]['hand']       = readers.csv(datapath, p, c, t, 'Hand.csv', hand_header)
            data[p][c][t]['hmd']        = readers.csv(datapath, p, c, t, 'HMD.csv', hmd_header)
            data[p][c][t]['gripper']    = readers.csv(datapath, p, c, t, 'Gripper.csv' , gripper_header)
            data[p][c][t]['robot']      = readers.csv(datapath, p, c, t, 'Robot.csv' , robot_header)
            
            time                        = data[p][c][t]['hand'] 
              
            #%% plot input path    
            plt.plot(time, data[p][c][t]['hand'].posZ) 
            fig3 = px.line_3d(data[p][c][t]['hand'], x='posZ', y='posX', z='posY', title = 'Hand input')
            plot(fig3, filename='plots/fig{}{}{}.html'.format(p,c,t,))