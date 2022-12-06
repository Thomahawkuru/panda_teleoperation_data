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
import pandas as pd

#%% define variables --------------------------------------------------------------------------------------------------
datapath        = os.getcwd() + "\\data\\"        # full path to read recorded data
savepath        = os.getcwd() + "\\save\\"        # full path to save calculated data
participants    = [0]                            # number of participants
conditions      = ['A', 'B', 'C', 'D', 'E', 'F']
columns_R       = ['RPos_X', 'RPos_Y', 'RPos_Z']
columns_L       = ['LPos_X', 'LPos_Y', 'LPos_Z']

exp_header      = [ "f", "dt", "t", "fps", "start", "hand", "Grip", "Tracked", "Controlling" ];
gaze_header     = [ "f", "dt", "t", "status", "gazeX", "gazeY", "gazeZ", "gazeposition", "focusdistance", "focusstability", "statusL", "LeftX", "LeftY", "LeftZ", "posL", "pupilL", "statusR", "RightX", "RightY", "RightZ", "positionR", "pupilR"];
hand_header     = [ "f", "dt", "t", "LposX", "LposY", "LposZ", "LrotX", "LrotY", "LrotZ", "LrotW", "Lgrab", "Lpinch", "RposX", "RPosY", "RposZ", "RrotX", "RrotY", "RrotZ", "RrotW", "Rgrab", "Rpinch"];
hand_hdr_short  = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grab", "pinch"];
hmd_header      = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ"];
gripper_header  = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grip_pos", "grip_vel", "grip_eff" ];
robot_header    = [ "f", "dt", "t", "tau1", "tau2", "tau3", "tau4", "tau5", "tau6", "tau7", "con_x", "con_y", "con_z" ];
    

#%% Read data ----------------------------------------------------------------------------------------------------------------------

for p in participants:
    handedness       = {}
    exp_data         = {}
    gaze_data        = {}
    hand_data        = {}
    hmd_data         = {}
    gripper_data     = {}
    robot_data       = {}
    time             = {} 
    
    print(), print(), print('Reading data for participant {}'.format(p))    
    handedness[p]       = readers.handedness(datapath,p)
    print('Handedeness {}'.format(handedness[p]))
    
    for c in conditions:     
        
        print(), print('Condition {}'.format(c))
        if c == "A": 
            continue
        
        exp_data[c]         = readers.csv(datapath, p, c, 'Experiment.csv', exp_header)
        gaze_data[c]        = readers.csv(datapath, p, c, 'Gaze.csv', gaze_header)
        hand_data[c]        = readers.csv(datapath, p, c, 'Hand.csv', hand_header)
        hmd_data[c]         = readers.csv(datapath, p, c, 'HMD.csv', hmd_header)
        gripper_data[c]     = readers.csv(datapath, p, c, 'Gripper.csv' , gripper_header)
        robot_data[c]       = readers.csv(datapath, p, c, 'Robot.csv' , robot_header)
        
        time[c]             = hand_data[c].t
       
#organize data based on handedness    
        if handedness[p] == 'R':
            hand_data[c].drop(list(hand_data[c].filter(regex = 'L')), axis=1, inplace=True)
            hand_data[c].columns = hand_hdr_short
            
        elif handedness[p] == 'L':
            hand_data[c].drop(list(hand_data[c].filter(regex = 'R')), axis=1, inplace=True)
            hand_data[c].columns = hand_hdr_short

    
        #%% plot input path    
        plt.plot(time[c], hand_data[c].posZ) 
        fig3 = px.line_3d(hand_data[c], x='posZ', y='posX', z='posY', title = 'Hand input')
        plot(fig3, filename='plots/fig3.html')