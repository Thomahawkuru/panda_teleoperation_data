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

#%% plot data    
dill.load_session('data_raw.pkl')

for p in Participants:
    for c in Conditions:
        for t in Trials:
            for f in Files:
                print('calculating')
# %%
