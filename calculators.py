# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:14:53 2022

@author: Thomas
"""

import numpy as np

def timestamps(experiment_data, savepath, participant, trail):
    spawns = max(experiment_data.TrailNumber) 
    
   
    #determine timestamps
    for i in range(2,len(experiment_data.Time)-1):
        i = 1
        
        
    return spawns

def velocity(data, columns):
    
    v = [0.0]
    data_3D = data[columns]
    
    for i in range(1,len(data_3D.iloc[:, 0])):
        dx = data_3D.iloc[i,0]-data_3D.iloc[i-1,0]
        dy = data_3D.iloc[i,1]-data_3D.iloc[i-1,1]
        dz = data_3D.iloc[i,2]-data_3D.iloc[i-1,2]
        
        v.append(np.sqrt(dx*dx + dy*dy + dz*dz))
        
    return v

