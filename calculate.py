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
    for c in Conditions:
        print(), print('Condition {}'.format(c))
        for t in Trials:
                fps = (data[p][c][t]['Experiment'].fps)
                print(fps)
# %%
