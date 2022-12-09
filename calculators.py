# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import numpy as np
import pandas as pd

def fps(data, p, c, t):
    fps = np.mean(data[p][c][t]['Experiment'].fps)

    return fps

def velocity(data, p, c, t, file):
    
    v = [0.0]
    data_3D = data[p][c][t][file][["posX", "posY", "posZ"]]
    
    for i in range(1,len(data_3D.iloc[:, 0])):
        dx = data_3D.iloc[i,0]-data_3D.iloc[i-1,0]
        dy = data_3D.iloc[i,1]-data_3D.iloc[i-1,1]
        dz = data_3D.iloc[i,2]-data_3D.iloc[i-1,2]
        
        v.append(np.sqrt(dx*dx + dy*dy + dz*dz))
        
    return v

