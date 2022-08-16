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
gaze_header     = [ "f", "dt", "t", "status", "gazeX", "gazeY", "gazeZ", "gazeposition", "focusdistance", "focusstability", "statusL", "LeftX", "LeftY", "LeftZ", "posL", "pupilL", "statusR", "RightX", "RightY", "RightZ", "positionR", "pupilR"];
hand_header     = [ "f", "dt", "t", "LposX", "LposY", "LposZ", "LrotX", "LrotY", "LrotZ", "LrotW", "Lgrab", "Lpinch", "RposX", "RPosY", "RposZ", "RrotX", "RrotY", "RrotZ", "RrotW", "Rgrab", "Rpinch"];
hand_hdr_short  = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "grab", "pinch"];
hmd_header      = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ"];
panda_header    = [ "f", "dt", "t", "posX", "posY", "posZ", "rotX", "rotY", "rotZ", "rotW", "gripper" ];
    

#%% Read data ----------------------------------------------------------------------------------------------------------------------
exp_data         = {}
gaze_data        = {}
hand_data        = {}
hmd_data         = {}
panda_data       = {}
time             = {}   
completion_times = {}
handedness       = {}


for p in range(1, participants + 1):
    print(), print(), print('Reading data for participant {}'.format(p))    
    
    exp_data[p]         = readers.csv(datapath, p, 'Experiment.csv', exp_header)
    gaze_data[p]        = readers.csv(datapath, p, 'Gaze.csv', gaze_header)
    hand_data[p]        = readers.csv(datapath, p, 'Hand.csv', hand_header)
    hmd_data[p]         = readers.csv(datapath, p, 'HMD.csv', hmd_header)
    panda_data[p]       = readers.csv(datapath, p, 'Panda.csv' , panda_header)
    
    time[p]             = hand_data[p].t
    completion_times[p] = readers.times(datapath, p)
    handedness[p]       = readers.handedness(datapath,p)

#organize data based on handedness    
    if handedness[p] == 'R':
        hand_data[p].drop(list(hand_data[p].filter(regex = 'L')), axis=1, inplace=True)
        hand_data[p].columns = hand_hdr_short
        
    elif handedness[p] == 'L':
        hand_data[p].drop(list(hand_data[p].filter(regex = 'R')), axis=1, inplace=True)
        hand_data[p].columns = hand_hdr_short

#%% Calculate data
print('Calculating velocity...')
input_velocity = {}
for p in range(1, participants + 1):
        input_velocity[p] = calculators.velocity(hand_data[p], ['posX', 'posY', 'posZ'])

print('Calculating ...')


#%% plot data
# completion time histogram
data = np.array(list(completion_times.items()))
fig1 = ff.create_distplot([data[:,1]], ['completion times [s]'])
plot(fig1, filename='plots/fig1.html')

#%% Plot velocity
fig2 = go.Figure()
for p in range(1, participants + 1):
    fig2.add_trace(go.Scatter(x=time[p], y=input_velocity[p], name='velocity', mode="lines"))
    fig2.add_trace(go.Scatter(x=time[p], y=hand_data[p].pinch/10, name='pinch', mode='lines'))    
    plot(fig2, filename='plots/fig2.html')
    
    
#%% plot input path    
plt.plot(time[2], hand_data[2].rotW) 
fig3 = px.line_3d(hand_data[1], x='posZ', y='posX', z='posY', title = 'Hand input')
plot(fig3, filename='plots/fig3.html')
#input_paths         = calcualtors.input_paths(timestamps, hand_data)