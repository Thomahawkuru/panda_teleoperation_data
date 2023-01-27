#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import dill
import seaborn as sns
import functions

dill.load_session('data_calculated.pkl')
Participants = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]                              # number of participants
Measures = ['Max', 'Med', 'Min', 'Avg']

#%% plot max/med/min/avg reache performance over all 3 trials  
fpss = []
times = []
track_err = []

for p in Participants:
    for c in Conditions[1:]:
        for t in Trials:
            fpss.append(data[p][c][t]['fps'])
            times.append(data[p][c][t]['duration'])
            track_err.append(data[p][c][t]['track_err']) 

fig1, ax1 = plt.subplots(3)
ax1[0].plot(fpss, 'b')
ax1[0].legend(["Average FPS [n]"])
ax1[1].plot(times, 'g')
ax1[1].legend(["Trial Duration [s]"])
ax1[1].set_ylim([59, 61])
ax1[2].plot(track_err,'r')
ax1[2].legend(["Tracking errors [n]"])
ax1[0].set_title('Sanity Checking, n = [{}]'.format(2*5*3))
fig1.savefig("plots/sanity_check.jpg")

#%% Load data into dataframes
grab_fails = pd.DataFrame([] , columns=['fails', 'participant', 'condition', 'measure'])
grab_succes = pd.DataFrame([] , columns=['succes', 'participant', 'condition', 'measure'])
grab_attempts = pd.DataFrame([] , columns=['attempts', 'participant', 'condition', 'measure'])
velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'measure'])
depth = pd.DataFrame([] , columns=['depth', 'participant', 'condition', 'measure'])

for p in Participants:
    for c in Conditions[1:]:
        for m in Measures:         
            new_row = functions.minmax(data, 'grabs', 'fail', p, c, m, Trials, Measures)
            grab_fails.loc[len(grab_fails)] = new_row
            new_row = functions.minmax(data, 'grabs', 'succes', p, c, m, Trials, Measures)
            grab_succes.loc[len(grab_succes)] = new_row
            new_row = functions.minmax(data, 'grabs', 'attempts', p, c, m, Trials, Measures)
            grab_attempts.loc[len(grab_attempts)] = new_row
            new_row = functions.minmax(data, 'velocity', None, p, c, m, Trials, Measures)
            velocity.loc[len(velocity)] = new_row
            new_row = functions.minmax(data, 'depth', None, p, c, m, Trials, Measures)
            depth.loc[len(depth)] = new_row  

fig2, ax2 = plt.subplots(5, 1, figsize=(5, 20))

sns.boxplot(x=grab_fails['condition'], y=grab_fails['fails'], hue=grab_fails['measure'], ax=ax2[0])
ax2[0].set_title('Failed Grabs [n={}]'.format(len(Participants)))
sns.boxplot(x=grab_succes['condition'], y=grab_succes['succes'], hue=grab_succes['measure'], ax=ax2[1])
ax2[1].set_title('Correct Grabs [n={}]'.format(len(Participants)))
sns.boxplot(x=grab_attempts['condition'], y=grab_attempts['attempts'], hue=grab_attempts['measure'], ax=ax2[2])
ax2[2].set_title('grab_attempts [n={}]'.format(len(Participants)))
sns.boxplot(x=velocity['condition'], y=velocity['velocity'], hue=velocity['measure'], ax=ax2[3])
ax2[3].set_title('Average Velocity [m/s]')
sns.boxplot(x=depth['condition'], y=depth['depth'], hue=depth['measure'], ax=ax2[4])
ax2[4].set_title('Input depth [m]')

fig2.tight_layout()
fig2.savefig("plots/trial_average.jpg")

#%% plot learning effects from trial 1 to 3
trial_velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'trial'])
trial_grabs = pd.DataFrame([] , columns=['attempts', 'succes', 'fails', 'participant', 'condition', 'trial'])
trail_depth = pd.DataFrame([] , columns=['depth', 'participant', 'condition', 'trial'])

for p in Participants:
    for c in Conditions[1:]:
        for t in Trials:         
            new_row = [np.mean(data[p][c][t]['velocity']), p, c, t]
            trial_velocity.loc[len(trial_velocity)] = new_row
            new_row = [data[p][c][t]['grabs']['attempts'], data[p][c][t]['grabs']['succes'], data[p][c][t]['grabs']['fail'], p, c, t]
            trial_grabs.loc[len(trial_grabs)] = new_row
            new_row = [data[p][c][t]['depth'], p, c, t]
            trail_depth.loc[len(trail_depth)] = new_row 

fig3, ax3 = plt.subplots(5, 1, figsize=(5, 20))

sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['fails'], hue=trial_grabs['trial'], ax=ax3[0])
ax3[0].set_title('Grab fails per trial [n={}]'.format(len(Participants)))
sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['succes'], hue=trial_grabs['trial'], ax=ax3[1])
ax3[1].set_title('Grab successes per trial [n={}]'.format(len(Participants)))
sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['attempts'], hue=trial_grabs['trial'], ax=ax3[2])
ax3[2].set_title('Grab attempts per trial [n={}]'.format(len(Participants)))
sns.boxplot(x=trial_velocity['condition'], y=trial_velocity['velocity'], hue=trial_velocity['trial'], ax=ax3[3])
ax3[3].set_title('Average input velocity per trial [n={}]'.format(len(Participants)))
sns.boxplot(x=trail_depth['condition'], y=trail_depth['depth'], hue=trail_depth['trial'], ax=ax3[4])
ax3[4].set_title('Input depth per trial [n={}]'.format(len(Participants)))

fig3.tight_layout()
fig3.savefig("plots/learning_effects.jpg")

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