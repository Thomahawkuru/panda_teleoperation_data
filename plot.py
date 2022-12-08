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
            plt.plot(data[p][c][t]['Hand'].posZ) 
            fig3 = px.line_3d(data[p][c][t]['Hand'], x='posZ', y='posX', z='posY', title = 'Hand input')
            plot(fig3, filename='plots/fig{}{}{}.html'.format(p,c,t,))
# %%
