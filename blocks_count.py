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

start = time.time()

# define variables --------------------------------------------------------------------------------------------------
root            = os.getcwd().replace("\\","/")
datapath        = root + "/data/Experiment/"        # full path to read recorded data
savepath        = root + "/save/"        # full path to save calculated data

Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]                      # Array of participants
Conditions      = ['A', 'B', 'C', 'D', 'E', 'F']
Trials          = [1, 2, 3]

# read questionnaire responses
print(), print('Reading blocks count csv')
Count   = pd.read_csv(datapath + "blocks_count.csv", delimiter=",", header=0).set_index('Participant Number')
# remove invalid participants:
for index, rows in Count.iterrows():
    if index not in Participants:
        Count = Count.drop(index)

Count = Count.reset_index().rename(columns={'index': 'original_index'})

# Decode questionaire responses
print('Decoding...')
# melt the dataframe
Count = pd.melt(Count, id_vars=['Participant Number'], value_name='blocks')
# split the variable column into separate columns for the letter and number
Count[['condition', 'trial']] = Count['variable'].str.extract('(\D)(\d)')
# drop the original variable column
Count = Count.drop('variable', axis=1)

#%% Calculating
print('Calculating...')

group = pd.DataFrame(Count.groupby(['Participant Number', 'condition'])['blocks'].mean())
group = group.reset_index().rename(columns={'index': 'original_index'})
group = group.melt(id_vars=['Participant Number', 'condition'], value_vars='blocks', value_name='blocks', var_name='trial')
group['trial'] = 'mean'
count_trail = pd.concat([Count,group],ignore_index=True)

count_minmax = Count
count_minmax['max'] = Count.groupby(['Participant Number', 'condition'])['blocks'].transform(np.maximum.reduce)
count_minmax['med'] = Count.groupby(['Participant Number', 'condition'])['blocks'].transform(np.median)
count_minmax['min'] = Count.groupby(['Participant Number', 'condition'])['blocks'].transform(np.minimum.reduce)
count_minmax['avg'] = Count.groupby(['Participant Number', 'condition'])['blocks'].transform(np.mean)
count_minmax = count_minmax.melt(id_vars=['Participant Number', 'condition'], value_vars=['max', 'med', 'min', 'avg'], \
                                 var_name ='measure', value_name='blocks')

#%% plotting
print('Plotting...')
fig8, ax8 = plt.subplots(2, 1, figsize=(7.5, 6))

sns.boxplot(x=count_trail['condition'][count_trail['condition'] != 'A'], y=count_trail['blocks'], hue=count_trail['trial'], ax=ax8[0])
ax8[0].set_title('Counted blocks per trial [n={}]'.format(len(Participants)))
ax8[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

sns.boxplot(x=count_minmax['condition'][count_minmax['condition'] != 'A'], y=count_minmax['blocks'], hue=count_minmax['measure'], ax=ax8[1])
ax8[1].set_title('Max, med, min and average counted blocks [n={}]'.format(len(Participants)))
ax8[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

fig8.tight_layout()
fig8.savefig("plots/blocks_count.jpg", dpi=1000)
fig8.savefig("plots/blocks_count.svg", dpi=1000)

#%% Evaluate
print('Evaluating...')
fig9, ax9 = plt.subplots(2, 4, figsize=(9, 4))
fig9.patch.set_visible(False)
trials = ['1', '2', '3', 'mean']
measures = ['max', 'med', 'min', 'avg']

for t in trials: 
    p_count_trial = pd.DataFrame(index = Conditions, columns = Conditions)

    for c1 in Conditions:
        for c2 in Conditions:
            diff_c1 = count_trail[(count_trail['condition']==c1) & (count_trail['trial']==t)]['blocks']
            diff_c2 = count_trail[(count_trail['condition']==c2) & (count_trail['trial']==t)]['blocks']
            p_value = np.round(stats.ttest_rel(diff_c1, diff_c2, nan_policy='omit') , 3)
            p_count_trial[c1][c2] = p_value[1]

    # plotting p-value tables
    functions.tablesubplot(ax9[0][trials.index(t)], p_count_trial, f'Trial {t} blocks')

for m in measures: 
    p_count_minmax = pd.DataFrame(index = Conditions, columns = Conditions)

    for c1 in Conditions:
        for c2 in Conditions:
            diff_c1 = count_minmax[(count_minmax['condition']==c1) & (count_minmax['measure']==m)]['blocks']
            diff_c2 = count_minmax[(count_minmax['condition']==c2) & (count_minmax['measure']==m)]['blocks']
            p_value = np.round(stats.ttest_rel(diff_c1, diff_c2, nan_policy='omit') , 3)
            p_count_minmax[c1][c2] = p_value[1]

    # plotting p-value tables
    functions.tablesubplot(ax9[1][measures.index(m)], p_count_minmax, f'{m} blocks')

fig9.tight_layout()
fig9.savefig("plots/p_values_blocks_count.jpg", dpi=1000)
fig9.savefig("plots/p_values_blocks_count.svg", dpi=1000)

#%% plot only average results
print('Average only...')

fig10, ax10 = plt.subplots(1, 2, figsize=(7.5, 2.5))

count_avg = count_minmax[count_minmax['measure'] == m]
sns.boxplot(x=count_avg['condition'][count_avg['condition'] != 'A'], y=count_avg['blocks'], hue=count_avg['measure'], ax=ax10[0])
ax10[0].set_title(f'{m} blocks transferred [n=3]')
ax10[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

# plotting p-value tables
functions.tablesubplot(ax10[1], p_count_minmax, f'{m} blocks transferred paired T-test p-values')

fig10.tight_layout()
fig10.savefig("plots/blocks_count_avg.jpg", dpi=1000)
fig10.savefig("plots/blocks_count_avg.svg", dpi=1000)

meanA = np.mean(count_minmax[count_minmax['condition'] == 'A'][count_minmax['measure'] == 'avg']['blocks'])
stdA = np.std(count_minmax[count_minmax['condition'] == 'A'][count_minmax['measure'] == 'avg']['blocks'])
print(f'Mean blocks transfered in Condition A: {meanA}')
print(f'SD of blocks transfered in Condition A: {stdA}')

#%% saving variables
print(), print('Dumping blocks count data to file...')
dill.dump_session('data_blocks_count.pkl')

end =  time.time()
print("Evaluation took: {}".format(end-start))