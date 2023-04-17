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

p = 0
t = 1

fig, ax= plt.subplots(2, 3, figsize=(10, 7.5), subplot_kw={'projection': '3d'})

ax[0,0].set_title('Condition A')
ax[0,1].plot( data[p]['B'][t]['Hand']['posX'],
                    data[p]['B'][t]['Hand']['posY'],
                    data[p]['B'][t]['Hand']['posZ'])
ax[0,1].set_title('Condition B')
ax[0,2].plot( data[p]['C'][t]['Hand']['posX'],
                    data[p]['C'][t]['Hand']['posY'],
                    data[p]['C'][t]['Hand']['posZ'])
ax[0,2].set_title('Condition C')
ax[1,0].plot( data[p]['D'][t]['Hand']['posX'],
                    data[p]['D'][t]['Hand']['posY'],
                    data[p]['D'][t]['Hand']['posZ'])
ax[1,0].set_title('Condition D')
ax[1,1].plot( data[p]['E'][t]['Hand']['posX'],
                    data[p]['E'][t]['Hand']['posY'],
                    data[p]['E'][t]['Hand']['posZ'])
ax[1,1].set_title('Condition E')
ax[1,2].plot( data[p]['F'][t]['Hand']['posX'],
                    data[p]['F'][t]['Hand']['posY'],
                    data[p]['F'][t]['Hand']['posZ'])
ax[1,2].set_title('Condition F')
fig.tight_layout

plt.show()
