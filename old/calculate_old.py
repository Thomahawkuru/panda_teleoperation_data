#%% import
import time
from plotly.offline import plot
import numpy as np
import dill
import pickle
import calculators
import warnings

dill.load_session('data_raw.pkl')
start = time.time()
Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26] # Array of participants

#%% plot data   
for p in Participants:
    print(), print(), print('Calculating data for participant {}'.format(p))
    for c in Conditions[1:]:
        print(), print('Condition {}'.format(c))
        for t in Trials:
            print('Trial {}'.format(t))
            
            data[p][c][t]['fps'] = calculators.fps(data, p, c, t)
            data[p][c][t]['duration'] = calculators.duration(data, p, c, t)
            data[p][c][t]['time'] = calculators.time(data, p, c, t)
            data[p][c][t]['track_err'] = calculators.track_error(data, p, c, t)       
            data[p][c][t]['grabs'] = calculators.grabs(data, p, c, t, debug=False)
            data[p][c][t]['velocity'] = calculators.grab_velocity(data, p, c, t, 'Hand', pre_time=2, debug=False)
            if c != 'B': #omit B because there is no HMD data
                data[p][c][t]['HMD'] = calculators.head_movement(data, p, c, t, debug=False)
            data[p][c][t]['in_out'] = calculators.in_out_corr(data, p, c, t, debug=False)  
            data[p][c][t]['force'] = calculators.force(data, p, c, t, debug=False)  
           
# %%
print(), print('Dumping calculated data to file...')
dill.dump_session('data_calculated.pkl')

end =  time.time()
print("Calculation time: {}".format(end-start))