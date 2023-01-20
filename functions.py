# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import os
import pandas
import numpy as np

def read_csv(path, participant, condition, trial, filename, header):
    # read data file
  
    participant_path = path + '{}\\'.format(str(participant))   
    
    trial_folder = [i for i in os.listdir(participant_path) if i.startswith(str(condition + '_'))]
    trial_path = participant_path + '{}\\'.format(trial_folder[trial-1]) 
    
    file = [i for i in os.listdir(trial_path) if os.path.isfile(os.path.join(trial_path, i)) and filename in i]
    
    csvdata = pandas.read_csv(trial_path + file[0], delimiter=",", header=0, names=header, skipfooter=1, engine='python')

    return csvdata

def crop_data(data_to_crop, check):
    
    data_cropped = data_to_crop.loc[check.start]

    track_check = filter_check(check.Tracked[check.start])
    data_tracked = data_cropped[track_check]

    control_check1 = filter_check(check.Controlling[check.start])
    control_check2 = control_check1[track_check]
    data_controlled = data_tracked[control_check2]

    return data_controlled

def filter_check(check): #removes data points just befor and just after a tracking error
    loc =  []

    for i in range(1,len(check)-1):
        if check.iloc[i] != check.iloc[i+1]:
            if check.iloc[i] == True:
                loc.append(i)
        if check.iloc[i] != check.iloc[i-1]:
            if check.iloc[i] == True:
                loc.append(i)

    check.iloc[loc] = False

    return check

def pdf(x):
    mean = np.mean(x)
    std = np.std(x)
    y_out = 1/(std * np.sqrt(2 * np.pi)) * np.exp( - (x - mean)**2 / (2 * std**2))
    return mean, std

def subplot(ax, df, title):
    ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center')
    ax.set_title(title)
    ax.axis('off')
    ax.axis('tight')