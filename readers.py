# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import os
import pandas
import math
import functions
import numpy as np

def handedness(path,participant):
    participant_folder = [i for i in os.listdir(path) if i.startswith(str(participant))]
    hand = participant_folder[0][2]
        
    return hand

def csv(path, participant, condition, filename, header):
    # read data file
  
    participant_folder = [i for i in os.listdir(path) if i.startswith(str(participant))]
    participant_path = path + '{}\\'.format(participant_folder[0])   
    
    trial_folder = [i for i in os.listdir(participant_path) if i.startswith(str(condition + '_'))]
    trial_path = participant_path + '{}\\'.format(trial_folder[0]) 
    
    file = [i for i in os.listdir(trial_path) if os.path.isfile(os.path.join(trial_path, i)) and filename in i]
    
    csvdata = pandas.read_csv(trial_path + file[0], delimiter=",", header=0, names=header)

    return csvdata

