#%% import
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import dill
import seaborn as sns
import functions

dill.load_session('data_plotted.pkl')

P = [0, 23]
t = 1

for p in P:
    fig, ax= plt.subplots(2, 3, figsize=(10, 7.5), subplot_kw={'projection': '3d'})

    ax[0,0].set_title('Condition A')
    ax[0,1].plot(   functions.crop_data(data[p]['B'][t]['Hand']['posX'], data[p]['B'][t]['Experiment']),
                    functions.crop_data(data[p]['B'][t]['Hand']['posY'], data[p]['B'][t]['Experiment']),
                    functions.crop_data(data[p]['B'][t]['Hand']['posZ'], data[p]['B'][t]['Experiment']))
    ax[0,1].set_title('Condition B')
    ax[0,2].plot(   functions.crop_data(data[p]['C'][t]['Hand']['posX'], data[p]['C'][t]['Experiment']),
                    functions.crop_data(data[p]['C'][t]['Hand']['posY'], data[p]['C'][t]['Experiment']),
                    functions.crop_data(data[p]['C'][t]['Hand']['posZ'], data[p]['C'][t]['Experiment']))
    ax[0,2].set_title('Condition C')
    ax[1,0].plot(   functions.crop_data(data[p]['D'][t]['Hand']['posX'], data[p]['D'][t]['Experiment']),
                    functions.crop_data(data[p]['D'][t]['Hand']['posY'], data[p]['D'][t]['Experiment']),
                    functions.crop_data(data[p]['D'][t]['Hand']['posZ'], data[p]['D'][t]['Experiment']))
    ax[1,0].set_title('Condition D')
    ax[1,1].plot(   functions.crop_data(data[p]['E'][t]['Hand']['posX'], data[p]['E'][t]['Experiment']),
                    functions.crop_data(data[p]['E'][t]['Hand']['posY'], data[p]['E'][t]['Experiment']),
                    functions.crop_data(data[p]['E'][t]['Hand']['posZ'], data[p]['E'][t]['Experiment']))
    ax[1,1].set_title('Condition E')
    ax[1,2].plot(   functions.crop_data(data[p]['F'][t]['Hand']['posX'], data[p]['F'][t]['Experiment']),
                    functions.crop_data(data[p]['F'][t]['Hand']['posY'], data[p]['F'][t]['Experiment']),
                    functions.crop_data(data[p]['F'][t]['Hand']['posZ'], data[p]['F'][t]['Experiment']))
    ax[1,2].set_title('Condition F')

    if p == 0:
        fig.suptitle(f'Input paths expert operator, trial {t}')
    else:
        fig.suptitle(f'Input paths for Participant {p}, trial {t}')
    fig.tight_layout

    plt.show()
