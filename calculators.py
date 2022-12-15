# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import numpy as np
import pandas as pd
import functions

def fps(data, p, c, t):
    fps = np.mean(data[p][c][t]['Experiment'].fps)

    return fps
def time(data, p, c, t):
    time = functions.crop_data(data[p][c][t]['Experiment']["t"], data[p][c][t]['Experiment'])
    time_rect = time - np.min(time)

    return time_rect

def velocity(data, p, c, t, file):
    
    v = [0.0]
    # crop data
    data_3D = data[p][c][t][file][["dt", "posX", "posY", "posZ"]]

    for i in range(1,len(data_3D.iloc[:, 0])):
        dx = data_3D.iloc[i,1]-data_3D.iloc[i-1,1]
        dy = data_3D.iloc[i,2]-data_3D.iloc[i-1,2]
        dz = data_3D.iloc[i,3]-data_3D.iloc[i-1,3]
        
        v.append(np.sqrt(dx*dx + dy*dy + dz*dz)/data_3D.iloc[i,0])
        
    velocity = functions.crop_data(pd.DataFrame(v), data[p][c][t]['Experiment']).to_numpy()

    return velocity