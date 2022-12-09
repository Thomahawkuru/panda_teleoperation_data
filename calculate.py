#%% import
import os
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pickle
import dill
import readers
import calculators

dill.load_session('data_raw.pkl')

#%% plot data   
for p in Participants:
    print(), print(), print('Calculating data for participant {}'.format(p))
    for c in Conditions[1:]:
        print(), print('Condition {}'.format(c))
        for t in Trials:
            fps = np.mean(data[p][c][t]['Experiment'].fps)
            print('Trial {}'.format(t), fps)
            data[p][c][t]['FPS'] = fps

# %%
dill.dump_session('data_calculated.pkl')
