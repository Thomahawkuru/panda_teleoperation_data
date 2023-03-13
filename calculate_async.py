#%% import
import time
from plotly.offline import plot
import numpy as np
import dill
import pickle
import calculators
import warnings
import _thread

def calculate_fps(data,p,c,t):
    data[p][c][t]['fps'] = calculators.fps(data, p, c, t)

def calculate_duration(data,p,c,t):
    data[p][c][t]['duration'] = calculators.duration(data, p, c, t)

def calculate_time(data,p,c,t):
    data[p][c][t]['time'] = calculators.time(data, p, c, t)

def calculate_tracking_err(data,p,c,t):
    data[p][c][t]['track_err'] = calculators.track_error(data, p, c, t)

def calculate_grabs(data,p,c,t):
    data[p][c][t]['grabs'] = calculators.grabs(data, p, c, t, debug=False)

def calculate_velocity(data,p,c,t):
    data[p][c][t]['velocity'] = calculators.grab_velocity(data, p, c, t, 'Hand', pre_time=2, debug=False)

def calculated_hmd(data,p,c,t):
    if c is not 'B':
        data[p][c][t]['HMD'] = calculators.head_movement(data, p, c, t, debug=False)

def calculated_corr(data,p,c,t):
    data[p][c][t]['in_out'] = calculators.in_out_corr(data, p, c, t, debug=False) 


dill.load_session('data_raw.pkl')
start = time.time()
Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]                      # Array of participants

#%% Calculate data   
for p in Participants:
    print(), print(), print('Calculating data for participant {}'.format(p))
    for c in Conditions[1:]:
        print(), print('Condition {}'.format(c))
        for t in Trials:
            print('Trial {}'.format(t))
            
            # calculate_fps(data,p,c,t)
            # calculate_duration(data,p,c,t)
            # calculate_time(data,p,c,t)
            # calculate_tracking_err(data,p,c,t)
            # calculate_grabs(data,p,c,t)
            # calculate_velocity(data,p,c,t)
            # calculated_hmd(data,p,c,t)
            # calculated_corr(data,p,c,t)
            # calculated_corr(data,p,c,t)  

            try:
                _thread.start_new_thread( calculate_fps, (data,p,c,t, ) )
                _thread.start_new_thread( calculate_duration, (data,p,c,t, ) )
                _thread.start_new_thread( calculate_time, (data,p,c,t, ) )
                _thread.start_new_thread( calculate_tracking_err, (data,p,c,t, ) )
                _thread.start_new_thread( calculate_grabs, (data,p,c,t, ) )
                _thread.start_new_thread( calculate_velocity, (data,p,c,t, ) )
                _thread.start_new_thread( calculated_hmd, (data,p,c,t, ) )
                _thread.start_new_thread( calculated_corr, (data,p,c,t, ) )
                _thread.start_new_thread( calculated_corr, (data,p,c,t, ) )

            except:
                print("Error: unable to start thread")
        
# %%
print(), print('Dumping calculated data to file...')
dill.dump_session('data_calculated.pkl')

end =  time.time()
print("Calculation time: {}".format(end-start))