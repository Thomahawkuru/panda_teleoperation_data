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

plot_start = time.time()
dill.load_session('data_calculated.pkl')
Measures = ['Mean [n=3]']
Participants    = [1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26] # Array of participants

#%% plot ming sanity check data
print(), print('Plotting sanity check') 
fpss =  pd.DataFrame([] , columns=['fps', 'participant', 'condition', 'trial'])
times =  pd.DataFrame([] , columns=['duration [s]', 'participant', 'condition', 'trial'])
track_err = pd.DataFrame([] , columns=['track_err', 'participant', 'condition', 'trial'])
input_lag = pd.DataFrame([] , columns=['lag [s]', 'participant', 'condition', 'trial'])

for p in Participants:
    for c in Conditions[1:]:
        for t in Trials:
            new_row = [np.mean(data[p][c][t]['fps']), p, c, t]
            fpss.loc[len(fpss)] = new_row 
            new_row = [np.mean(data[p][c][t]['duration']), p, c, t]
            times.loc[len(times)] = new_row 
            new_row = [np.mean(data[p][c][t]['track_err']), p, c, t]
            track_err.loc[len(track_err)] = new_row
            new_row = [np.mean(data[p][c][t]['in_out']['lag']), p, c, t]
            input_lag.loc[len(track_err)] = new_row 
#%%
fpss = fpss.groupby(['participant', 'condition'])['fps'].mean().reset_index()
times = times.groupby(['participant', 'condition'])['duration [s]'].mean().reset_index()
track_err = track_err.groupby(['participant', 'condition'])['track_err'].mean().reset_index()
input_lag = input_lag.groupby(['participant', 'condition'])['lag [s]'].mean().reset_index()

fig1, ax1 = plt.subplots(4,2,figsize=(7.5,10))
sns.boxplot(x=fpss['condition'], y=fpss['fps'], ax=ax1[0,0])
ax1[0,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
ax1[0,0].set_title(f'Average FPS per condition [n=3]')
sns.boxplot(x=times['condition'], y=times['duration [s]'], ax=ax1[1,0])
ax1[1,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
ax1[1,0].set_title(f'Average duration per condition [n=3]')
sns.boxplot(x=track_err['condition'], y=track_err['track_err'], ax=ax1[2,0])
ax1[2,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
ax1[2,0].set_title(f'Tracking losses per condition [n=3]')
sns.boxplot(x=input_lag['condition'], y=input_lag['lag [s]'], ax=ax1[3,0])
ax1[3,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
ax1[3,0].set_title(f'Average input Lag per condition [n=3]')

fig1.tight_layout()
fig1.savefig("plots/sanity_check.jpg", dpi=1000)
fig1.savefig("plots/sanity_check.svg", dpi=1000)

#%% plot avg reache performance over all 3 trials 
print(), print('Plotting avg boxplots') 

grabs = pd.DataFrame([] , columns=['count', 'participant', 'condition', 'measure'])
velocity = pd.DataFrame([] , columns=['pre', 'post', 'participant', 'condition', 'measure'])
hmd_movement = pd.DataFrame([] , columns=['std', 'participant', 'condition', 'measure'])
in_out_corr = pd.DataFrame([] , columns=['corr', 'participant', 'condition', 'measure'])
force = pd.DataFrame([] , columns=['force', 'participant', 'condition', 'measure'])

for p in Participants:
    for c in Conditions[1:]:
        avg_attempts = np.mean([data[p][c][1]['grabs']['attempts'],data[p][c][2]['grabs']['attempts'],data[p][c][3]['grabs']['attempts']])          
        new_row = [avg_attempts, p, c, 'attempts']
        grabs.loc[len(grabs)] = new_row
        avg_success = np.mean([data[p][c][1]['grabs']['success'],data[p][c][2]['grabs']['success'],data[p][c][3]['grabs']['success']])
        new_row = [avg_success, p, c, 'success']
        grabs.loc[len(grabs)] = new_row
        avg_fails = np.mean([data[p][c][1]['grabs']['fail'],data[p][c][2]['grabs']['fail'],data[p][c][3]['grabs']['fail']])
        new_row = [avg_fails, p, c, 'fails']
        grabs.loc[len(grabs)] = new_row

        for m in Measures:
            new_row = [data[p][c][t]['velocity']['pre'], data[p][c][t]['velocity']['post'], p, c, m]
            velocity.loc[len(velocity)] = new_row
            if c == 'B':
                new_row = [0, p, c, m]
            else: 
                new_row = functions.minmax(data, 'HMD', 'rotation', p, c, m, Trials, Measures)            
            hmd_movement.loc[len(hmd_movement)] = new_row  
            new_row = functions.minmax(data, 'in_out', 'max_corr', p, c, m, Trials, Measures)
            in_out_corr.loc[len(in_out_corr)] = new_row
            new_row = functions.minmax(data, 'force', None, p, c, m, Trials, Measures)
            force.loc[len(force)] = new_row  

fig2, ax2 = plt.subplots(8, 2, figsize=(7.5, 16))

ax_span = plt.subplot(8,1,1)
sns.boxplot(x=grabs['condition'], y=grabs['count'], hue=grabs['measure'], ax=ax_span)
ax_span.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

print('Average only...')
for p in Participants:
    count_p = count_avg[count_avg['Participant Number']==p]
    for c in Conditions[1:]:
        count_c = count_p[count_p['condition']==c]     
        new_row = [count_c['blocks'].mean(), p, c, 'transfer']
        grabs.loc[len(grabs)] = new_row

grabs['count'] = pd.to_numeric(grabs['count'], errors='coerce')
ax_span.cla()
order = ['attempts', 'fails', 'success', 'transfer']
sns.boxplot(x=grabs['measure'], y=grabs['count'], hue=grabs['condition'], ax=ax_span, order=order)
ax_span.set_title('Average grab  data over 3 trials')
ax_span.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

sns.boxplot(x=velocity['condition'], y=velocity['pre'], hue=velocity['measure'], ax=ax2[3,0])
ax2[3,0].set_title('Average Pre-Grab Velocity [m/s]', wrap=True)
ax2[3,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=velocity['condition'], y=velocity['post'], hue=velocity['measure'], ax=ax2[4,0])
ax2[4,0].set_title('Average Post-Grab Velocity [m/s]', wrap=True)
ax2[4,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=hmd_movement['condition'], y=hmd_movement['std'], hue=hmd_movement['measure'], ax=ax2[5,0])
ax2[5,0].set_title('Rotational SD of HMD direction unit vector', wrap=True)
ax2[5,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=in_out_corr['condition'], y=in_out_corr['corr'], hue=in_out_corr['measure'], ax=ax2[6,0])
ax2[6,0].set_title('Input-Output Cross-correlation', wrap=True)
ax2[6,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=force['condition'], y=force['force'], hue=force['measure'], ax=ax2[7,0])
ax2[7,0].set_title('Average peak force [N]', wrap=True)
ax2[7,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

meanA = np.mean(count_avg[count_avg['condition'] == 'A']['blocks'])
stdA = np.std(count_avg[count_avg['condition'] == 'A']['blocks'])
print(f'Mean blocks transfered in Condition A: {meanA}')
print(f'SD of blocks transfered in Condition A: {stdA}')

fig2.tight_layout()
fig2.savefig("plots/average_results.jpg", dpi=1000)
fig2.savefig("plots/average_results.svg", dpi=1000)

print(), print('Dumping plotted data to file...')
dill.dump_session('data_plotted.pkl')
end =  time.time()
print("Plotting time: {}".format(end-plot_start))