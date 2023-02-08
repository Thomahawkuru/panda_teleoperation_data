#%% import
import os
import time
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import pickle
import dill
import functions

start = time.time()

# define variables --------------------------------------------------------------------------------------------------
root            = os.getcwd().replace("\\","/")
datapath        = root + "/data/Experiment/"        # full path to read recorded data
savepath        = root + "/save/"        # full path to save calculated data

Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]                      # Array of participants
Conditions      = ['A', 'B', 'C', 'D', 'E', 'F']
Trials          = [1, 2, 3]

#%% read questionnaire responses
Questionnaire = pd.read_csv(datapath + "responses.csv", delimiter=",", header=0)
Questionnaire = Questionnaire.set_index('Participant number:')