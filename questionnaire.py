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
import dill
import seaborn as sns

start = time.time()

# define variables --------------------------------------------------------------------------------------------------
root            = os.getcwd().replace("\\","/")
datapath        = root + "/data/Experiment/"        # full path to read recorded data
savepath        = root + "/save/"        # full path to save calculated data

Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]                      # Array of participants
Conditions      = ['A', 'B', 'C', 'D', 'E', 'F']
Trials          = [1, 2, 3]

opnion_header = ['condition', 'hand', 'trial 1', 'comment 1','trial 2', 'comment 2', 'trial 3', 'comment 3', 'requirements', 'frustration', 'easyness', 'correcting']

#%% read questionnaire responses ----------------------------------------------------------------
print(), print('Reading questionnaire csv')
Questionnaire   = pd.read_csv(datapath + "responses.csv", delimiter=",", header=0).set_index('Participant number:')
Demographic     = Questionnaire.iloc[:,range(10)]

# remove invalid participants:
for index, rows in Questionnaire.iterrows():
    if index not in Participants:
        Questionnaire = Questionnaire.drop(index)

#%% Decode questionaire responses ---------------------------------------------------------------
print('Decoding...')
questQuestionnaire = Questionnaire.replace([1,2,3,4,5,6,7], [-3,-2,-1,0,1,2,3])

Questionnaire = Questionnaire.replace('Strongly agree', 3)
Questionnaire = Questionnaire.replace('.....', 2)
Questionnaire = Questionnaire.replace('....', 1)
Questionnaire = Questionnaire.replace('...', 0)
Questionnaire = Questionnaire.replace('..', -1)
Questionnaire = Questionnaire.replace('.', -2)
Questionnaire = Questionnaire.replace('Strongly disagree', -3)

Questionnaire = Questionnaire.replace('Right hand', 'R')
Questionnaire = Questionnaire.replace('Left hand', 'L')

results = pd.DataFrame()
Opinions = {}

for i in range(6):
    Opinions[i] = Questionnaire.iloc[:,10:].iloc[:,range(0+12*i,12+12*i)]
    Opinions[i] = Opinions[i].set_axis(opnion_header, axis=1).drop(columns=['comment 1','comment 2','comment 3'])

for c in Conditions:
    Opinions[c] = pd.DataFrame()

    for i in range(6):
        new_rows = Opinions[i][Opinions[i].iloc[:,0].str.startswith('Condition {}'.format(c))]
        Opinions[c] = pd.concat([Opinions[c], new_rows]).sort_index()
        Opinions[c]['condition'] = c
        
    results = pd.concat([results, Opinions[c]])

#%% plot responses
print('Plotting...')
difficulty = results.iloc[:,range(5)].melt(['condition','hand'], var_name='trial',value_name='difficulty')
usefullness = results[['condition', 'requirements', 'frustration', 'easyness', 'correcting']]
usefullness = usefullness.melt(['condition'], var_name='measure',value_name='opinion')

fig4, ax4 = plt.subplots(2, 1, figsize=(7.5, 8))

sns.boxplot(x=difficulty['condition'], y=difficulty['difficulty'], hue=difficulty['trial'], ax=ax4[0])
ax4[0].set_title('Perceived Easiness per trial [n={}]'.format(len(Participants)))
ax4[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

sns.boxplot(x=usefullness['measure'], y=usefullness['opinion'], hue=usefullness['condition'], ax=ax4[1])
ax4[1].set_title('UMUX results per condition [n={}]'.format(len(Participants)))
ax4[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)


fig4.tight_layout()
fig4.savefig("plots/questionnaire.jpg")

#%% evaluate responses
print('Evaluating...')

#%% saving variables
print(), print('Dumping questionnaire data to file...')
dill.dump_session('data_questionnaire.pkl')

end =  time.time()
print("Evaluation took: {}".format(end-start))