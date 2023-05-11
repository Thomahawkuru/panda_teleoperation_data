#%% import
import time
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import dill
import seaborn as sns
import functions

plot_start = time.time()
dill.load_session('data_evaluated.pkl')
Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26] # Array of participants

#%% produce data
grabs = grabs.sort_values(by=["participant","condition","measure"]).reset_index(drop=True)
velocity = velocity.sort_values(by=["participant","condition","measure"]).reset_index(drop=True)
hmd_movement = hmd_movement.sort_values(by=["participant","condition","measure"]).reset_index(drop=True)
in_out_corr = in_out_corr.sort_values(by=["participant","condition","measure"]).reset_index(drop=True)
force = force.sort_values(by=["participant","condition","measure"]).reset_index(drop=True)

grabs.to_csv("data/eval/grabs.csv")
velocity.to_csv("data/eval/velocity.csv")
hmd_movement.to_csv("data/eval/hmd_movement.csv")
in_out_corr.to_csv("data/eval/in_out_corr.csv")
force.to_csv("data/eval/force.csv")

#sanity checking data
fpss =  fpss.sort_values(by=["participant","condition","trial"]).reset_index(drop=True)
times =  times.sort_values(by=["participant","condition","trial"]).reset_index(drop=True)
track_err = track_err.sort_values(by=["participant","condition","trial"]).reset_index(drop=True)
input_lag = input_lag.sort_values(by=["participant","condition","trial"]).reset_index(drop=True)

fpss.to_csv("data/eval/fpss.csv")
times.to_csv("data/eval/completion_times.csv")
track_err.to_csv("data/eval/track_err.csv")
input_lag.to_csv("data/eval/input_lag.csv")
