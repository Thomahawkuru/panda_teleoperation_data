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
import math

plot_start = time.time()
dill.load_session('data_calculated.pkl')
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
            new_row = [np.nanmean(data[p][c][t]['fps']), p, c, t]
            fpss.loc[len(fpss)] = new_row 
            new_row = [np.nanmean(data[p][c][t]['duration']), p, c, t]
            times.loc[len(times)] = new_row 
            new_row = [np.nanmean(data[p][c][t]['track_err']), p, c, t]
            track_err.loc[len(track_err)] = new_row
            new_row = [np.nanmean(data[p][c][t]['in_out']['lag']), p, c, t]
            input_lag.loc[len(track_err)] = new_row 
#%%
fpss = fpss.groupby(['participant', 'condition'])['fps'].mean().reset_index()
times = times.groupby(['participant', 'condition'])['duration [s]'].mean().reset_index()
track_err = track_err.groupby(['participant', 'condition'])['track_err'].mean().reset_index()
input_lag = input_lag.groupby(['participant', 'condition'])['lag [s]'].mean().reset_index()

fig1, ax1 = plt.subplots(4,2,figsize=(7.5,10))
sns.boxplot(x=fpss['condition'], y=fpss['fps'], ax=ax1[0,0])
ax1[0,0].set_title(f'Average FPS per condition [n=3]')
sns.boxplot(x=times['condition'], y=times['duration [s]'], ax=ax1[1,0])
ax1[1,0].set_title(f'Average duration per condition [n=3]')
sns.boxplot(x=track_err['condition'], y=track_err['track_err'], ax=ax1[2,0])
ax1[2,0].set_title(f'Tracking losses per condition [n=3]')
sns.boxplot(x=input_lag['condition'], y=input_lag['lag [s]'], ax=ax1[3,0])
ax1[3,0].set_title(f'Average input Lag per condition [n=3]')

fig1.tight_layout()
fig1.savefig("plots/sanity_check.jpg", dpi=1000)
fig1.savefig("plots/sanity_check.svg", dpi=1000)

#%% Calculated average data over 3 trials
print(), print('Calculating averages') 

grabs = pd.DataFrame([] , columns=['count', 'participant', 'condition', 'measure'])
velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'measure'])
hmd_movement = pd.DataFrame([] , columns=['std', 'participant', 'condition', 'measure'])
in_out_corr = pd.DataFrame([] , columns=['corr', 'participant', 'condition', 'measure'])
force = pd.DataFrame([] , columns=['force', 'participant', 'condition', 'measure'])

for p in Participants:
    count_p = count_avg[count_avg['Participant Number']==p]
    for c in Conditions[1:]:
        # grab data
        avg_attempts = functions.trial_average(data, 'grabs', 'attempts', p, c, Trials)          
        new_row = [avg_attempts, p, c, 'attempts']
        grabs.loc[len(grabs)] = new_row
        avg_success = functions.trial_average(data, 'grabs', 'success', p, c, Trials)  
        new_row = [avg_success, p, c, 'success']
        grabs.loc[len(grabs)] = new_row
        avg_fails = functions.trial_average(data, 'grabs', 'fail', p, c, Trials)  
        new_row = [avg_fails, p, c, 'fails']
        grabs.loc[len(grabs)] = new_row
        count_c = count_p[count_p['condition']==c]     
        new_row = [count_c['blocks'].mean(), p, c, 'transfer']
        grabs.loc[len(grabs)] = new_row

        # velocity data
        avg_pre_vel = functions.trial_average(data, 'velocity', 'pre', p, c, Trials)  
        new_row = [avg_pre_vel, p, c, 'pre']
        velocity.loc[len(velocity)] = new_row
        avg_post_vel = functions.trial_average(data, 'velocity', 'post', p, c, Trials)  
        new_row = [avg_post_vel, p, c, 'post']
        velocity.loc[len(velocity)] = new_row
        
        # other data
        if c == 'B':
            new_row = [0, p, c, 'Mean [n=3]']
        else: 
            new_row = functions.trial_average(data, 'HMD', 'rotation', p, c, Trials)            
        hmd_movement.loc[len(hmd_movement)] = new_row  
        avg_hmd_movement = functions.mintrial_averagemax(data, 'force', None, p, c, Trials)
        new_row = [avg_hmd_movement, p, c, 'Mean [N=3]']
        force.loc[len(force)] = new_row  
        avg_force = functions.trial_average(data, 'in_out', 'max_corr', p, c, Trials)
        new_row = [avg_force, p, c, 'Mean [N=3]']
        in_out_corr.loc[len(in_out_corr)] = new_row

grabs['count'] = pd.to_numeric(grabs['count'], errors='coerce')

#%% plotting
print(), print('Plotting barplots') 
fig2, ax2 = plt.subplots(4, 2, figsize=(7.5, 16))

# grab data
order = ['attempts', 'fails', 'success', 'transfer']
functions.error_bar_plot(grabs, 'count', order, plt.subplot(4,1,1), 'Average grab data [n=3]', Participants, Conditions[1:])

# velocities
order = ['pre', 'post']
functions.error_bar_plot(velocity, 'velocity', order, plt.subplot(4,1,2), 'Average Pre- and Post-Grab Velocity [m/s]', Participants, Conditions[1:])

# other measures
order = ['Mean [n=3]']
functions.error_bar_plot(hmd_movement, 'std',   order, ax2[2,0], 'Rotational SD of HMD direction unit vector', Participants, Conditions[1:])
functions.error_bar_plot(force,        'force', order, ax2[2,1], 'Average peak force [N]', Participants, Conditions[1:])
functions.error_bar_plot(in_out_corr,  'corr',  order, ax2[3,0], 'Input-Output Cross-correlation', Participants, Conditions[1:])

fig2.tight_layout()
fig2.savefig("plots/average_results.jpg", dpi=1000)
fig2.savefig("plots/average_results.svg", dpi=1000)

# Data for condition A
meanA = np.mean(count_avg[count_avg['condition'] == 'A']['blocks'])
stdA = np.std(count_avg[count_avg['condition'] == 'A']['blocks'])
print(f'Mean blocks transfered in Condition A: {meanA}')
print(f'SD of blocks transfered in Condition A: {stdA}')

# saving data
print(), print('Dumping plotted data to file...')
dill.dump_session('data_plotted.pkl')
end =  time.time()
print("Plotting time: {}".format(end-plot_start))