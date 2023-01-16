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

#%% plot sanity check data    
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
ax1[2].plot(track_err,'r')
ax1[2].legend(["Tracking errors [n]"])
ax1[0].set_title('Sanity Checking, n = [{}]'.format(2*5*3))
fig1.savefig("plots/sanity_check.jpg")

#%% plot data per condition
failed_grabs = pd.DataFrame()
correct_grabs = pd.DataFrame()
grab_attempts = pd.DataFrame()
average_velocity = pd.DataFrame()
input_depth = pd.DataFrame()

for c in Conditions[1:]:
    Fails = []
    Succes = []
    Grabs = []
    Velocity = []
    Depth = []

    for p in Participants:
        failed = 0
        correct = 0
        grabs = 0
        velocity = 0
        depth = 0

        for t in Trials:
            failed += data[p][c][t]['grabs']['fail']
            correct += data[p][c][t]['grabs']['succes']
            grabs += data[p][c][t]['grabs']['attempts']
            velocity += np.mean(data[p][c][t]['velocity'])
            depth += data[p][c][t]['depth']
        
        Velocity.append(velocity/3)
        Fails.append(failed/3)
        Grabs.append(grabs/3)
        Succes.append(correct/3)
        Depth.append(depth/3)

    failed_grabs[c] = Fails
    correct_grabs[c] = Succes
    grab_attempts[c] = Grabs
    average_velocity[c] = Velocity
    input_depth[c] = Depth

fig2, ax2 = plt.subplots()
ax2.boxplot(failed_grabs, whis=[0, 100], showmeans=True)
ax2.set_title('Failed Grabs [Average n]')
ax2.set_xlabel('Conditions')
ax2.set_xticklabels(['B','C','D','E','F'])
fig2.savefig("plots/failed_grabs.jpg")

fig3, ax3 = plt.subplots()
ax3.boxplot(correct_grabs, whis=[0, 100], showmeans=True)
ax3.set_title('Correct Grabs [Average n]')
ax3.set_xticklabels(['B','C','D','E','F'])
ax3.set_xlabel('Conditions')
fig3.savefig("plots/correct_grabs.jpg")

fig4, ax4 = plt.subplots()
ax4.boxplot(average_velocity, whis=[0, 100], showmeans=True)
ax4.set_title('Average Velocity [m/s]')
ax4.set_xlabel('Conditions')
ax4.set_xticklabels(['B','C','D','E','F'])
fig4.savefig("plots/average_velocity.jpg")

fig5, ax5 = plt.subplots()
ax5.boxplot(input_depth, whis=[0, 100], showmeans=True)
ax5.set_title('Input depth [m]')
ax5.set_xlabel('Conditions')
ax5.set_xticklabels(['B','C','D','E','F'])
fig5.savefig("plots/input_depth.jpg")

fig6, ax6 = plt.subplots()
ax6.boxplot(grab_attempts, whis=[0, 100], showmeans=True)
ax6.set_title('grab_attempts [Average n]')
ax6.set_xticklabels(['B','C','D','E','F'])
ax6.set_xlabel('Conditions')
fig6.savefig("plots/grab_attempts.jpg")

#%% plot learning effects in average trial velocity and grab attempts
trial_velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'trial'])
trial_grabs = pd.DataFrame([] , columns=['attempts', 'succes', 'fails', 'participant', 'condition', 'trial'])

for p in Participants:
    for c in Conditions[1:]:
        for t in Trials:         
            new_row = [np.mean(data[p][c][t]['velocity']), p, c, t]
            trial_velocity.loc[len(trial_velocity)] = new_row
            new_row = [data[p][c][t]['grabs']['attempts'], data[p][c][t]['grabs']['succes'], data[p][c][t]['grabs']['fail'], p, c, t]
            trial_grabs.loc[len(trial_grabs)] = new_row            

fig7, ax7 = plt.subplots(1,4, figsize=(20, 5))
sns.boxplot(x=trial_velocity['condition'], y=trial_velocity['velocity'], hue=trial_velocity['trial'], ax=ax7[0])
ax7[0].set_title('Average input velocity per trial [n={}]'.format(len(Participants)))
sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['attempts'], hue=trial_grabs['trial'], ax=ax7[1])
ax7[1].set_title('Grab attempts per trial [n={}]'.format(len(Participants)))
sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['succes'], hue=trial_grabs['trial'], ax=ax7[2])
ax7[2].set_title('Grab successes per trial [n={}]'.format(len(Participants)))
sns.boxplot(x=trial_grabs['condition'], y=trial_grabs['fails'], hue=trial_grabs['trial'], ax=ax7[3])
ax7[3].set_title('Grab fails per trial [n={}]'.format(len(Participants)))

fig7.savefig("plots/learning_effects.jpg")

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