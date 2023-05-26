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

# add average over trials

results['average'] = results[['trial 1', 'trial 2', 'trial 3']].mean(axis=1)

#%% plot responses
print('Plotting...')
difficulty = results.iloc[:,[0,1,2,3,4,9]].melt(['condition','hand'], var_name='trial',value_name='difficulty')
usefullness = results[['condition', 'requirements', 'frustration', 'easiness', 'correcting']]
usefullness = usefullness.melt(['condition'], var_name='measure',value_name='opinion')

fig4, ax4 = plt.subplots(1, 2, figsize=(7.5, 2.5))
avg_difficulty = difficulty[difficulty['trial']=='average']
sns.barplot(x=avg_difficulty['trial'], y=avg_difficulty['difficulty'], hue=avg_difficulty['condition'], ax=ax4[0], errorbar=('ci',95), capsize = 0.05, errwidth=1)
ax4[0].set_title('Average perceived Easiness [errorbar = CI 95]'.format(len(Participants)))
ax4[0].set_xticks([], [])
ax4[0].set_xlabel('Conditions'), ax4[0].set_ylabel('Average Easiness')
ax4[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

fig5, ax5 = plt.subplots(3, 2, figsize=(7.5, 7.5))
fig5.patch.set_visible(False)
ax = plt.subplot(3, 1, 1)
sns.barplot(x=usefullness['measure'], y=usefullness['opinion'], hue=usefullness['condition'], ax=ax, errorbar=('ci',95), capsize = 0.05, errwidth=1)
ax.set_title('UMUX results per condition [errorbar = CI 95]'.format(len(Participants)))
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

#%% evaluate SEQ responses
print('Evaluating...')
trials = ['average']

for t in trials: 
    p_difficulty = pd.DataFrame(index = Conditions, columns = Conditions)

    for c1 in Conditions:
        for c2 in Conditions:
            diff_c1 = difficulty[(difficulty['condition']==c1) & (difficulty['trial']==t)]['difficulty']
            diff_c2 = difficulty[(difficulty['condition']==c2) & (difficulty['trial']==t)]['difficulty']
            p_value = np.round(stats.ttest_rel(diff_c1, diff_c2, nan_policy='omit') , 3)
            p_difficulty[c1][c2] = p_value[1]

    # plotting p-value tables
    functions.tablesubplot(ax4[1], p_difficulty, f'{t} Easiness paired T-test p-values')

fig4.tight_layout()
fig4.savefig("plots/difficulty.jpg", dpi=1000)
fig4.savefig("plots/difficulty.svg", dpi=1000)

#%% evaluate UMUX responses
measures = ['requirements', 'frustration', 'easiness', 'correcting']

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
        functions.tablesubplot(ax5[1][measures.index(m)], p_usefullness, f'{m} paired T-test p-values')
    else:
        functions.tablesubplot(ax5[2][measures.index(m)-2], p_usefullness, f'{m} paired T-test p-values')
    
fig5.tight_layout()
fig5.savefig("plots/usefullness.jpg", dpi=1000)
fig5.savefig("plots/usefullness.svg", dpi=1000)

#%% saving variables
print(), print('Dumping questionnaire data to file...')
dill.dump_session('data_questionnaire.pkl')

end =  time.time()
print("Evaluation took: {}".format(end-questionaire_start))