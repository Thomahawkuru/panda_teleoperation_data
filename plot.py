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

Measures = ['Avg']

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

#%% plot avg reache performance over all 3 trials 
print(), print('Plotting avg boxplots') 

grab_fails = pd.DataFrame([] , columns=['fails', 'participant', 'condition', 'measure'])
grab_succes = pd.DataFrame([] , columns=['succes', 'participant', 'condition', 'measure'])
grab_attempts = pd.DataFrame([] , columns=['attempts', 'participant', 'condition', 'measure'])
pre_velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'measure'])
post_velocity = pd.DataFrame([] , columns=['velocity', 'participant', 'condition', 'measure'])
hmd_movement = pd.DataFrame([] , columns=['std', 'participant', 'condition', 'measure'])
in_out_corr = pd.DataFrame([] , columns=['corr', 'participant', 'condition', 'measure'])
force = pd.DataFrame([] , columns=['force', 'participant', 'condition', 'measure'])

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
            new_row = functions.minmax(data, 'force', None, p, c, m, Trials, Measures)
            force.loc[len(force)] = new_row  

fig2, ax2 = plt.subplots(8, 2, figsize=(7.5, 21))

sns.boxplot(x=grab_fails['condition'], y=grab_fails['fails'], hue=grab_fails['measure'], ax=ax2[0,0])
ax2[0,0].set_title('Failed Grabs [n={}]'.format(len(Participants)))
ax2[0,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=grab_succes['condition'], y=grab_succes['succes'], hue=grab_succes['measure'], ax=ax2[1,0])
ax2[1,0].set_title('Correct Grabs [n={}]'.format(len(Participants)))
ax2[1,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=grab_attempts['condition'], y=grab_attempts['attempts'], hue=grab_attempts['measure'], ax=ax2[2,0])
ax2[2,0].set_title('grab_attempts [n={}]'.format(len(Participants)))
ax2[2,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=pre_velocity['condition'], y=pre_velocity['velocity'], hue=pre_velocity['measure'], ax=ax2[3,0])
ax2[3,0].set_title('Average Pre-Grab Velocity [m/s]')
ax2[3,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=post_velocity['condition'], y=post_velocity['velocity'], hue=post_velocity['measure'], ax=ax2[4,0])
ax2[4,0].set_title('Average Post-Grab Velocity [m/s]')
ax2[4,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=hmd_movement['condition'], y=hmd_movement['std'], hue=post_velocity['measure'], ax=ax2[5,0])
ax2[5,0].set_title('Rotational SD of HMD movement')
ax2[5,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=in_out_corr['condition'], y=in_out_corr['corr'], hue=in_out_corr['measure'], ax=ax2[6,0])
ax2[6,0].set_title('Input-Output Correlation')
ax2[6,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
sns.boxplot(x=force['condition'], y=force['force'], hue=force['measure'], ax=ax2[7,0])
ax2[7,0].set_title('Average peak force [N]')
ax2[7,0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

fig2.tight_layout()
fig2.savefig("plots/avg.jpg", dpi=1000)
fig2.savefig("plots/avg.svg", dpi=1000)

# %%
print(), print('Dumping plotted data to file...')
dill.dump_session('data_plotted.pkl')

end =  time.time()
print("Plotting time: {}".format(end-start))