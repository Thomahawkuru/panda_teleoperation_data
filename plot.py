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

dill.load_session('data_calculated.pkl')
start = time.time()

Measures = ['Max', 'Med', 'Min', 'Avg']

#%% plot ming sanity check data
print(), print('Plotting sanity check') 
fpss =  pd.DataFrame([] , columns=['fps', 'participant', 'condition', 'trial'])
times =  pd.DataFrame([] , columns=['duration', 'participant', 'condition', 'trial'])
track_err = pd.DataFrame([] , columns=['track_err', 'participant', 'condition', 'trial'])

for p in Participants:
    for c in Conditions[1:]:
        for t in Trials:
            new_row = [np.mean(data[p][c][t]['fps']), p, c, t]
            fpss.loc[len(fpss)] = new_row 
            new_row = [np.mean(data[p][c][t]['duration']), p, c, t]
            times.loc[len(times)] = new_row 
            new_row = [np.mean(data[p][c][t]['track_err']), p, c, t]
            track_err.loc[len(track_err)] = new_row 

fig1, ax1 = plt.subplots(3)
sns.boxplot(x=fpss['condition'], y=fpss['fps'], hue=fpss['trial'], ax=ax1[0])
ax1[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=times['condition'], y=times['duration'], hue=times['trial'], ax=ax1[1])
ax1[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=track_err['condition'], y=track_err['track_err'], hue=track_err['trial'], ax=ax1[2])
ax1[2].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

ax1[0].set_title('Sanity Checking, n = [{}]'.format(2*5*3))
fig1.tight_layout()
fig1.savefig("plots/sanity_check.jpg", dpi=1000)
fig1.savefig("plots/sanity_check.svg", dpi=1000)

#%% plot max/med/min/avg reache performance over all 3 trials 
print(), print('Plotting min/max/avg boxplots') 

grab_fails = pd.DataFrame([] , columns=['fails', 'participant', 'condition', 'measure'])
grab_succes = pd.DataFrame([] , columns=['succes', 'participant', 'condition', 'measure'])
grab_attempts = pd.DataFrame([] , columns=['attempts', 'participant', 'condition', 'measure'])
pre_velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'measure'])
post_velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'measure'])
hmd_movement = pd.DataFrame([] , columns=['std', 'participant', 'condition', 'measure'])
in_out_corr = pd.DataFrame([] , columns=['corr', 'participant', 'condition', 'measure'])

for p in Participants:
    for c in Conditions[1:]:
        for m in Measures:         
            new_row = functions.minmax(data, 'grabs', 'fail', p, c, m, Trials, Measures)
            grab_fails.loc[len(grab_fails)] = new_row
            new_row = functions.minmax(data, 'grabs', 'succes', p, c, m, Trials, Measures)
            grab_succes.loc[len(grab_succes)] = new_row
            new_row = functions.minmax(data, 'grabs', 'attempts', p, c, m, Trials, Measures)
            grab_attempts.loc[len(grab_attempts)] = new_row
            new_row = functions.minmax(data, 'velocity', 'pre', p, c, m, Trials, Measures)
            pre_velocity.loc[len(pre_velocity)] = new_row
            new_row = functions.minmax(data, 'velocity', 'post', p, c, m, Trials, Measures)
            post_velocity.loc[len(post_velocity)] = new_row           
            if c == 'B':
                new_row = [0, p, c, m]
            else: 
                new_row = functions.minmax(data, 'HMD', 'rotation', p, c, m, Trials, Measures)            
            hmd_movement.loc[len(hmd_movement)] = new_row  
            new_row = functions.minmax(data, 'in_out', None, p, c, m, Trials, Measures)
            in_out_corr.loc[len(in_out_corr)] = new_row 

fig2, ax2 = plt.subplots(7, 1, figsize=(7.5, 21))

sns.boxplot(x=grab_fails['condition'], y=grab_fails['fails'], hue=grab_fails['measure'], ax=ax2[0])
ax2[0].set_title('Failed Grabs [n={}]'.format(len(Participants)))
ax2[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=grab_succes['condition'], y=grab_succes['succes'], hue=grab_succes['measure'], ax=ax2[1])
ax2[1].set_title('Correct Grabs [n={}]'.format(len(Participants)))
ax2[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=grab_attempts['condition'], y=grab_attempts['attempts'], hue=grab_attempts['measure'], ax=ax2[2])
ax2[2].set_title('grab_attempts [n={}]'.format(len(Participants)))
ax2[2].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=pre_velocity['condition'], y=pre_velocity['velocity'], hue=pre_velocity['measure'], ax=ax2[3])
ax2[3].set_title('Average Pre-Grab Velocity [m/s]')
ax2[3].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=post_velocity['condition'], y=post_velocity['velocity'], hue=post_velocity['measure'], ax=ax2[4])
ax2[4].set_title('Average Post-Grab Velocity [m/s]')
ax2[4].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=hmd_movement['condition'], y=hmd_movement['std'], hue=post_velocity['measure'], ax=ax2[5])
ax2[5].set_title('Rotational SD of HMD movement')
ax2[5].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=in_out_corr['condition'], y=in_out_corr['corr'], hue=in_out_corr['measure'], ax=ax2[6])
ax2[6].set_title('Input-Output Correlation')
ax2[6].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

fig2.tight_layout()
fig2.savefig("plots/min_max_avg.jpg", dpi=1000)
fig2.savefig("plots/min_max_avg.svg", dpi=1000)

#%% plot learning effects from trial 1 to 3
print(), print('Plotting learning effect boxplots') 

trial_velocity = pd.DataFrame([] , columns=['pre', 'post', 'participant', 'condition', 'trial'])
trial_grabs = pd.DataFrame([] , columns=['attempts', 'succes', 'fails', 'participant', 'condition', 'trial'])
trial_hmd = pd.DataFrame([] , columns=['std', 'participant', 'condition', 'trial'])
trial_corr = pd.DataFrame([] , columns=['corr', 'participant', 'condition', 'trial'])

for p in Participants:
    for c in Conditions[1:]:
        for t in Trials:         
            new_row = [data[p][c][t]['velocity']['pre'], data[p][c][t]['velocity']['post'], p, c, t]
            trial_velocity.loc[len(trial_velocity)] = new_row
            new_row = [data[p][c][t]['grabs']['attempts'], data[p][c][t]['grabs']['succes'], data[p][c][t]['grabs']['fail'], p, c, t]
            trial_grabs.loc[len(trial_grabs)] = new_row
            
            if c == 'B':
                new_row = [0, p, c, t]
            else:
                new_row = [data[p][c][t]['HMD']["rotation"], p, c, t]
            
            trial_hmd.loc[len(trial_hmd)] = new_row
            new_row = [data[p][c][t]['in_out'], p, c, t]
            trial_corr.loc[len(trial_corr)] = new_row

fig3, ax3 = plt.subplots(7, 1, figsize=(7.5, 21))

sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['fails'], hue=trial_grabs['trial'], ax=ax3[0])
ax3[0].set_title('Grab fails per trial [n={}]'.format(len(Participants)))
ax3[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['succes'], hue=trial_grabs['trial'], ax=ax3[1])
ax3[1].set_title('Grab successes per trial [n={}]'.format(len(Participants)))
ax3[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['attempts'], hue=trial_grabs['trial'], ax=ax3[2])
ax3[2].set_title('Grab attempts per trial [n={}]'.format(len(Participants)))
ax3[2].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=trial_velocity['condition'], y=trial_velocity['pre'], hue=trial_velocity['trial'], ax=ax3[3])
ax3[3].set_title('Average pre-grab velocity per trial [n={}]'.format(len(Participants)))
ax3[3].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=trial_velocity['condition'], y=trial_velocity['post'], hue=trial_velocity['trial'], ax=ax3[4])
ax3[4].set_title('Average post-grab velocity per trial [n={}]'.format(len(Participants)))
ax3[4].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=trial_hmd['condition'], y=trial_hmd['std'], hue=trial_hmd['trial'], ax=ax3[5])
ax3[5].set_title('Rotational SD of HMD movement [n={}]'.format(len(Participants)))
ax3[5].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=trial_corr['condition'], y=trial_corr['corr'], hue=trial_corr['trial'], ax=ax3[6])
ax3[6].set_title('Input-Output Correlation[n={}]'.format(len(Participants)))
ax3[6].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

fig3.tight_layout()
fig3.savefig("plots/learning_effects.jpg", dpi=1000)
fig3.savefig("plots/learning_effects.svg", dpi=1000)

# %% plot input paths
# for p in [8]:
#     for c in ['B', 'C']:
#         for t in [1]:
#             plot_data = functions.crop_data(data[p][c][t]['Hand'][['posZ','posX','posY']],data[p][c][t]['Experiment'])
#             fig3 = px.line_3d(plot_data, x='posZ', y='posX', z='posY', title = 'Hand input')
#             plot(fig3, filename='plots/fig{}{}{}.html'.format(p,c,t,))

# %%
print(), print('Dumping plotted data to file...')
dill.dump_session('data_plotted.pkl')

end =  time.time()
print("Plotting time: {}".format(end-start))