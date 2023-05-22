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

def read_blocks_count(datapath,Participants):
    Count   = pandas.read_csv(datapath + "blocks_count.csv", delimiter=",", header=0).set_index('Participant Number')
    # remove invalid participants:
    for index, rows in Count.iterrows():
        if index not in Participants:
            Count = Count.drop(index)

    Count = Count.reset_index().rename(columns={'index': 'original_index'})

    # Decode questionaire responses
    print('Decoding...')
    # melt the dataframe
    Count = pandas.melt(Count, id_vars=['Participant Number'], value_name='blocks')
    # split the variable column into separate columns for the letter and number
    Count[['condition', 'trial']] = Count['variable'].str.extract('(\D)(\d)')
    # drop the original variable column
    Count = Count.drop('variable', axis=1) 

    return Count

def crop_data(data_to_crop, check):       
    data_cropped = data_to_crop.loc[check.start]
    
    tracked = check.Tracked[check.start]
    track_check = filter_check(tracked)
    data_tracked = data_cropped[track_check]

    controlling = check.Controlling[check.start]
    control_check1 = filter_check(controlling)
    control_check2 = control_check1[track_check]
    data_controlled = data_tracked[control_check2]

    return data_controlled

def filter_check(check): #removes data points just befor and just after a tracking error
    i = 0
    while i < len(check)-1:
        i += 1
        if check.iloc[i-1] == True and check.iloc[i] == False:
            check.iloc[i-1] = False
            i += 1
        if check.iloc[i-1] == False and check.iloc[i] == True:
            check.iloc[i:i+60] = False
            i += 61 

    return check

def pdf(x):
    mean = np.mean(x,axis=0)
    std = np.std(x,axis=0)
    y_out = 1/(std * np.sqrt(2 * np.pi)) * np.exp( - (x - mean)**2 / (2 * std**2))
    return mean, std

def tablesubplot(ax, df, title):
    nrows, ncols = df.shape
    colors = []
    cell_text = []

    for i in range(nrows):
        colors_in_column = ["w"] * ncols
        row_text = []
        for j in range(ncols):
            if j > i:
                colors_in_column[j] = "w"  # Set cell color to white if above diagonal
                row_text.append("")  # Set empty string for cells above the diagonal
            else:
                value = df.iloc[i, j]
                if value <= 0.05:
                    colors_in_column[j] = "g"  # Set cell color to green if value is <= 0.05
                row_text.append("{:.3f}".format(value))  # Set cell text for cells on or below the diagonal
        colors.append(colors_in_column)
        cell_text.append(row_text)

    ax.table(cellText=cell_text, colLabels=df.columns, rowLabels=df.index, loc='center', cellColours=colors)
    ax.set_title(title, wrap=True)
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
    if type is not None:
        measure_data = data[data[type] == m]
    else:
        measure_data=data

    p_value = np.around(
        stats.ttest_rel(
            measure_data[measure_data['condition']==c1][key], 
            measure_data[measure_data['condition']==c2][key],
            nan_policy='omit')
        , 3)

    return p_value

def grab_start_end(grab_crop, peaks_succes):
    startpoints = []
    endpoints = []

    threshold = 0.3 #-0.0395
    
    start = False
    
    for i in range(len(peaks_succes)):
        j = peaks_succes[i]

        while grab_crop[j] < threshold:
            j -= 1
            if j < 0:
                j = peaks_succes[i]
                break

        while grab_crop[j] > threshold and start == False:
            j -= 1
            if grab_crop[j] < threshold or j == 0:
                startpoints.append(j)    
                start = True

        while start == True:
            j += 1

            if j < len(grab_crop):
                if grab_crop[j] < threshold:             
                    endpoints.append(j)    
                    start = False
            elif j == len(grab_crop):
                startpoints.remove(startpoints[-1])
                j -= 1
                start = False

    return startpoints, endpoints

def pre_grap_location(input_data, startpoints, pre_time):
    prepoints = []

    for i in range(len(startpoints)):
        t = 0
        j = 0

        while t < pre_time:
            j += 1
            try: 
                t += input_data.loc[startpoints[i]-j]['dt']    
            except KeyError:
                t = pre_time
                j -= 1
                
        prepoint = startpoints[i] - j
        prepoints.append(prepoint)
        #print('pre-start dist: {}'.format(startpoints[i] - j))
    
    return prepoints

def avg_velocity(data_3D):
    v = []
    
    for i in range(1,len(data_3D.iloc[:, 0])):
        dx = data_3D.iloc[i,1]-data_3D.iloc[i-1,1]
        dy = data_3D.iloc[i,2]-data_3D.iloc[i-1,2]
        dz = data_3D.iloc[i,3]-data_3D.iloc[i-1,3]
        
        v.append(np.sqrt(dx*dx + dy*dy + dz*dz)/data_3D.iloc[i,0])

    avg_v = np.mean(v)

    return avg_v

