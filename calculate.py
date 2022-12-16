#%% import
import os
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import dill
import calculators

dill.load_session('data_raw.pkl')

#%% plot data   
for p in Participants:
    print(), print(), print('Calculating data for participant {}'.format(p))
    for c in Conditions[1:]:
        print(), print('Condition {}'.format(c))
        for t in Trials:
            print('Trial {}'.format(t))
            
            data[p][c][t]['fps'] = calculators.fps(data, p, c, t)
            print('FPS: {}'.format(data[p][c][t]['fps']))
            
            data[p][c][t]['duration'] = calculators.duration(data, p, c, t)
            print('Duration: {}'.format(data[p][c][t]['duration']))
            
            data[p][c][t]['time'] = calculators.time(data, p, c, t)
           
            data[p][c][t]['velocity'] = calculators.velocity(data, p, c, t, 'Hand')
            print('Velocity: {}'.format(np.mean(data[p][c][t]['velocity'])))            
            
            data[p][c][t]['grabs'] = calculators.grabs(data, p, c, t)
            print('Succes: {}'.format(data[p][c][t]['grabs']['succes']))  
            print('Fail: {}'.format(data[p][c][t]['grabs']['fail']))   

            print()

# %%
print(), print('Dumping calculated data to file...')
dill.dump_session('data_calculated.pkl')
