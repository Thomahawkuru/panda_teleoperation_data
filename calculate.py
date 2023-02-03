#%% import
import time
from plotly.offline import plot
import numpy as np
import dill
import pickle
import calculators

dill.load_session('data_raw.pkl')
start = time.time()
Participants = Participants[1:]                              # number of participants

#%% plot data   
for p in Participants:
    print(), print(), print('Calculating data for participant {}'.format(p))
    for c in Conditions[1:]:
        print(), print('Condition {}'.format(c))
        for t in Trials:
            print('Trial {}'.format(t))
            
            data[p][c][t]['fps'] = calculators.fps(data, p, c, t)
            #print('FPS: {}'.format(data[p][c][t]['fps']))
            
            data[p][c][t]['duration'] = calculators.duration(data, p, c, t)
            #print('Duration: {}'.format(data[p][c][t]['duration']))

            data[p][c][t]['time'] = calculators.time(data, p, c, t)

            data[p][c][t]['track_err'] = calculators.track_error(data, p, c, t)
            #print('Tracking errors: {}'.format(data[p][c][t]['track_err']))
                      
            data[p][c][t]['grabs'] = calculators.grabs(data, p, c, t)
            #print('Succes: {}'.format(data[p][c][t]['grabs']['succes']))  
            #print('Fail: {}'.format(data[p][c][t]['grabs']['fail']))   

            data[p][c][t]['velocity'] = calculators.grab_velocity(data, p, c, t, 'Hand', 1)
            #print('Velocity: {}'.format(np.mean(data[p][c][t]['velocity'])))            
           
# %%
print(), print('Dumping calculated data to file...')
dill.dump_session('data_calculated.pkl')

end =  time.time()
print("Calculation time: {}".format(end-start))