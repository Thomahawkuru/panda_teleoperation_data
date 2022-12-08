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

def csv(path, participant, condition, trial, filename, header):
    # read data file
  
    participant_path = path + '{}\\'.format(str(participant))   
    
    trial_folder = [i for i in os.listdir(participant_path) if i.startswith(str(condition + '_'))]
    trial_path = participant_path + '{}\\'.format(trial_folder[trial-1]) 
    
    file = [i for i in os.listdir(trial_path) if os.path.isfile(os.path.join(trial_path, i)) and filename in i]
    
    csvdata = pandas.read_csv(trial_path + file[0], delimiter=",", header=0, names=header, skipfooter=1, engine='python')

    return csvdata

