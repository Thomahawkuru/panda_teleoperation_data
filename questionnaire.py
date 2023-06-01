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
from scipy import stats
import dill
import seaborn as sns
import functions

questionaire_start = time.time()
dill.load_session('data_raw.pkl')

Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26] # Array of participants
opnion_header   = ['condition', 'hand', 'trial 1', 'comment 1','trial 2', 'comment 2', 'trial 3', 'comment 3', 'requirements', 'frustration', 'easiness', 'correcting']
measures        = opnion_header[-4:]
trials          = ['trial 1', 'trial 2', 'trial 3', 'average']

#%% Decode questionaire responses ---------------------------------------------------------------
print('Decoding...')
Questionnaire = Questionnaire.replace([1,2,3,4,5,6,7], [-3,-2,-1,0,1,2,3])

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

# remove outliers
results = results[results.index.isin(Participants)]
results = results.reset_index().rename(columns={'Participant number:': 'participant'})

# add average over trials
results['average'] = results[['trial 1', 'trial 2', 'trial 3']].mean(axis=1)

#%% plot responses
print('Plotting...')

difficulty = results.iloc[:,[0,1,2,3,4,5,10]].melt(['participant','condition','hand'], var_name='measure',value_name='difficulty')
avg_difficulty = difficulty[difficulty['measure']=='average']
usefullness = results[['participant','condition', 'requirements', 'frustration', 'easiness', 'correcting']]
usefullness = usefullness.melt(['participant','condition'], var_name='measure',value_name='opinion')

fig4, ax4 = plt.subplots(4, 2, figsize=(7.5, 8))
CI = functions.error_bar_plot(difficulty, 'difficulty', trials, plt.subplot(2,1,1), 'SEQ results per trial', Participants, Conditions)

fig5, ax5 = plt.subplots(4, 2, figsize=(7.5, 8))
CI = CI.append(functions.error_bar_plot(usefullness, 'opinion', measures, plt.subplot(2, 1, 1), 'UMUX results per condition', Participants, Conditions))

print('Questionnaire CI:')
print(CI)

#%% evaluate SEQ responses
print('Evaluating...')

p_difficulty = pd.DataFrame(index = Conditions, columns = Conditions)

for t in trials:
    for c1 in Conditions:
        for c2 in Conditions:
            diff_c1 = difficulty[(difficulty['condition']==c1) & (difficulty['measure']==t)]['difficulty']
            diff_c2 = difficulty[(difficulty['condition']==c2) & (difficulty['measure']==t)]['difficulty']
            p_value = np.round(stats.ttest_rel(diff_c1, diff_c2, nan_policy='omit') , 3)
            p_difficulty[c1][c2] = p_value[1]

    # plotting p-value tables
    if trials.index(t) < 2:
        functions.tablesubplot(ax4[2][trials.index(t)], p_difficulty, f'{t} SEQ paired T-test p-values')
    else:
        functions.tablesubplot(ax4[3][trials.index(t)-2], p_difficulty, f'{t} SEQ paired T-test p-values')

fig4.tight_layout()
fig4.savefig("plots/difficulty.jpg", dpi=1000)
fig4.savefig("plots/difficulty.svg", dpi=1000)

#%% evaluate UMUX responses

for m in measures: 
    p_usefullness= pd.DataFrame(index = Conditions, columns = Conditions)

    for c1 in Conditions:
        for c2 in Conditions:
            use_c1 = usefullness[(usefullness['condition']==c1) & (usefullness['measure']==m)]['opinion']
            use_c2 = usefullness[(usefullness['condition']==c2) & (usefullness['measure']==m)]['opinion']
            p_value = np.round(stats.ttest_rel(use_c1, use_c2, nan_policy='omit') , 3)
            p_usefullness[c1][c2] = p_value[1]

    # plotting p-value tables
    if measures.index(m) < 2:
        functions.tablesubplot(ax5[2][measures.index(m)], p_usefullness, f'{m} paired T-test p-values')
    else:
        functions.tablesubplot(ax5[3][measures.index(m)-2], p_usefullness, f'{m} paired T-test p-values')
    
fig5.tight_layout()
fig5.savefig("plots/usefullness.jpg", dpi=1000)
fig5.savefig("plots/usefullness.svg", dpi=1000)

#%% saving variables
print(), print('Dumping questionnaire data to file...')
dill.dump_session('data_questionnaire.pkl')

end =  time.time()
print("Evaluation took: {}".format(end-questionaire_start))