# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import os
import pandas
import numpy as np
from scipy import stats

def read_csv(path, participant, condition, trial, filename, header):
    # read data file
  
    participant_path = path + '{}/'.format(str(participant))   
    
    trial_folder = [i for i in os.listdir(participant_path) if i.startswith(str(condition + '_'))]
    trial_path = participant_path + '{}/'.format(trial_folder[trial-1]) 
    
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

def tablesubplot(ax, df, title):
    colors = []
    
    for _ , row in df.iterrows():
        colors_in_column = ["w"]*len(df)
        for idx in row.index:    
            if row[idx] < 0.05:                    
                colors_in_column[row.index.get_loc(idx)] = "g"

            elif 0.05 <= row[idx] < 0.1:
                colors_in_column[row.index.get_loc(idx)] = "y"

        
        colors.append(colors_in_column)

    ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellColours=colors)
    ax.set_title(title)
    ax.axis('off')
    ax.axis('tight')

def minmax(data, key, type, p, c, m, T, M):
    values = []
    if type == None:
        for t in T:
            values.append(np.mean(data[p][c][t][key]))
    else:
        for t in T:
            values.append(np.mean(data[p][c][t][key][type]))

    if m == M[0]:
        row = [np.max(values), p, c, m]
    elif m == M[1]:
        row = [np.median(values), p, c, m]
    elif m == M[2]:
        row = [np.min(values), p, c, m]
    elif m == M[3]:
        row = [np.average(values), p, c, m]

    return row

def p_values(data, key, m, c1, c2, type):

    measure_data = data[data[type] == m]
    p_value = np.round(
        stats.ttest_rel(
            measure_data[measure_data['condition']==c1][key], 
            measure_data[measure_data['condition']==c2][key])
        ,3)

    return p_value