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


def csv(path, participant, filename, header):
    # read data file
    trialpath = path + '{}/'.format(participant) 
    file = [i for i in os.listdir(trialpath) if os.path.isfile(os.path.join(trialpath, i)) and \
            filename in i]
    
    csvdata = pandas.read_csv(trialpath + file[0], delimiter=",", header=None, names=header)

    return csvdata

def times(path,participant):
    trialpath = path + '{}/'.format(participant) 
    folders = os.listdir(trialpath)
    time = 0.0;
    
    for name in folders:
        check = name.replace('.', '', 1).isdigit()
        if check == True:
            time = float(name)
            break
    
    print(time)
    return time

def handedness(path,participant):
    trialpath = path + '{}/'.format(participant) 
    folders = os.listdir(trialpath)
    hand = ''
    
    for name in folders:
        if name[0] == 'L':
            hand = 'L'
            break
        elif name[0] == 'R':
            hand = 'R'
            break
        
    print(hand)
    return hand

