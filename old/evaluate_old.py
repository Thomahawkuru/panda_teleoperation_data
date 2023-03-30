#%%
import time
import pandas as pd
import numpy as np
import dill
import matplotlib.pyplot as plt
from scipy import stats
import functions

dill.load_session('data_plotted.pkl')
start = time.time()

#%% determine unvalid participant trials
unvalid = pd.DataFrame([] , columns=['fps 1', 'fps 2', 'fps 3', 'duration 1', 'duration 2', 'duration 3', 'track_err 1', 'track_err 2', 'track_err 3'])

for p in Participants:
    unvalid.loc[p] = ['', '', '','', '', '','', '', '']

    for c in Conditions[1:]:
        for t in Trials:
            if data[p][c][t]['fps'] < 55:
                unvalid[f'fps {t}'][p] = np.round(data[p][c][t]['fps'],1)
            if data[p][c][t]['duration'] < 59.9:
                unvalid[f'duration {t}'][p] = np.round(data[p][c][t]['duration'],1)
            if data[p][c][t]['track_err'] > 0:
                unvalid[f'track_err {t}'][p] = data[p][c][t]['track_err']

print(), print('Validation data for participant: ') 
print(unvalid)

#%% calculating p_values for min/med/max/avg measures
print(), print('Calculating P-value tables over all trials')

fig4, ax4 = plt.subplots(7, 4, figsize=(12, 14))
fig4.patch.set_visible(False)

for m in Measures:
    print("Measure: {}".format(m))
    
    p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_succes = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_pre_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_post_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_hmd_movement = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_correlation = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

    for c1 in Conditions[1:]:
        for c2 in Conditions[1:]:

            _, p_grab_fails[c1][c2] = functions.p_values(grab_fails, 'fails', m, c1, c2, 'measure')
            _, p_grab_succes[c1][c2] = functions.p_values(grab_succes, 'succes', m, c1, c2, 'measure')
            _, p_grab_attemts[c1][c2] = functions.p_values(grab_attempts, 'attempts', m, c1, c2, 'measure')
            _, p_pre_velocity[c1][c2] = functions.p_values(pre_velocity, 'velocity', m, c1, c2, 'measure')
            _, p_post_velocity[c1][c2] = functions.p_values(post_velocity, 'velocity', m, c1, c2, 'measure')
            if c1 != 'B' and c2 != 'B':
                _, p_hmd_movement[c1][c2] = functions.p_values(hmd_movement, 'std', m, c1, c2, 'measure')
            _, p_correlation[c1][c2] = functions.p_values(in_out_corr, 'corr', m, c1, c2, 'measure')

    # plotting p-value tables
    functions.tablesubplot(ax4[0][Measures.index(m)], p_grab_fails, '{} Failed Grabs'.format(m))
    functions.tablesubplot(ax4[1][Measures.index(m)], p_grab_succes, '{} Correct grabs'.format(m))
    functions.tablesubplot(ax4[2][Measures.index(m)], p_grab_attemts, '{} Grab attempts'.format(m))
    functions.tablesubplot(ax4[3][Measures.index(m)], p_pre_velocity, '{} Pre-Grab Velocity'.format(m))
    functions.tablesubplot(ax4[4][Measures.index(m)], p_post_velocity, '{} Post-Grab Velocity'.format(m))
    functions.tablesubplot(ax4[5][Measures.index(m)], p_hmd_movement, '{} HMD rotational SD'.format(m))
    functions.tablesubplot(ax4[6][Measures.index(m)], p_correlation, '{} Input-Output Correlation'.format(m))
    
fig4.tight_layout()
fig4.savefig("plots/p_values_min_max.jpg".format(m), dpi=1000)
fig4.savefig("plots/p_values_min_max.svg".format(m), dpi=1000)

#%% calculating p_values for trial 1-3 learning effects
print(), print('Calculating P-value tables for learning effects')
fig5, ax5 = plt.subplots(7, 3, figsize=(9, 14))
fig5.patch.set_visible(False)

for t in Trials:
    print("Trial: {}".format(t))
    
    p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_succes = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_pre_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_post_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_hmd_movement = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_correlation = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

    for c1 in Conditions[1:]:
        for c2 in Conditions[1:]:

            _, p_grab_fails[c1][c2] = functions.p_values(trial_grabs, 'fails', t, c1, c2, 'trial')
            _, p_grab_succes[c1][c2] = functions.p_values(trial_grabs, 'succes', t, c1, c2, 'trial')
            _, p_grab_attemts[c1][c2] = functions.p_values(trial_grabs, 'attempts', t, c1, c2, 'trial')
            _, p_pre_velocity[c1][c2] = functions.p_values(trial_velocity, 'pre', t, c1, c2, 'trial')
            _, p_post_velocity[c1][c2] = functions.p_values(trial_velocity, 'post', t, c1, c2, 'trial')
            if c1 != 'B' and c2 != 'B':
                _, p_hmd_movement[c1][c2] = functions.p_values(trial_hmd, 'std', t, c1, c2, 'trial')
            _, p_correlation[c1][c2] = functions.p_values(trial_corr, 'corr', t, c1, c2, 'trial')

    # plotting p-value tables
    functions.tablesubplot(ax5[0][t-1], p_grab_fails, 'Failed Grabs Trial {}'.format(t))
    functions.tablesubplot(ax5[1][t-1], p_grab_succes, 'Correct grabs Trial {}'.format(t))
    functions.tablesubplot(ax5[2][t-1], p_grab_attemts, 'Grab attempts Trial {}'.format(t))
    functions.tablesubplot(ax5[3][t-1], p_pre_velocity, 'Pre-Grab Velocity Trial {}'.format(t))
    functions.tablesubplot(ax5[4][t-1], p_post_velocity, 'Post-Grab Velocity Trial {}'.format(t))
    functions.tablesubplot(ax5[5][t-1], p_hmd_movement, 'HMD rotational SD Trial {}'.format(t))
    functions.tablesubplot(ax5[6][t-1], p_correlation, 'Input-Output Correlation Trial {}'.format(t))

fig5.tight_layout()
fig5.savefig("plots/p_values_learning.jpg".format(t), dpi=1000)
fig5.savefig("plots/p_values_learning.svg".format(t), dpi=1000)

#%% saving variables
print(), print('Dumping evaluated data to file...')
dill.dump_session('data_evaluated.pkl')

end =  time.time()
print("Evaluation time: {}".format(end-start))