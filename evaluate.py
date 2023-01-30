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
unvalid = pd.DataFrame([] , columns=['fps', 'duration', 'track_err'])

for p in Participants:
    unvalid.loc[p] = ['', '', '']

    for c in Conditions[1:]:
        for t in Trials:
            if data[p][c][t]['fps'] < 55:
                unvalid['fps'][p] = data[p][c][t]['fps']
            if data[p][c][t]['duration'] < 59.9:
                unvalid['duration'][p] = data[p][c][t]['fps']
            if data[p][c][t]['track_err'] > 5:
                unvalid['track_err'][p] = data[p][c][t]['track_err']

print(), print('Unvalid data for participant: ') 
print(unvalid)

#%% calculating p_values for min/med/max/avg measures
print(), print('Calculating P-value tables over all trials')

fig4, ax4 = plt.subplots(5, 4, figsize=(12, 10))
fig4.patch.set_visible(False)

for m in Measures:
    print("Measure: {}".format(m))
    
    p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_succes = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_input_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_input_depth = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

    for c1 in Conditions[1:]:
        for c2 in Conditions[1:]:

            _, p_grab_fails[c1][c2] = functions.p_values(grab_fails, 'fails', m, c1, c2, 'measure')
            _, p_grab_succes[c1][c2] = functions.p_values(grab_succes, 'succes', m, c1, c2, 'measure')
            _, p_grab_attemts[c1][c2] = functions.p_values(grab_attempts, 'attempts', m, c1, c2, 'measure')
            _, p_input_velocity[c1][c2] = functions.p_values(velocity, 'velocity', m, c1, c2, 'measure')
            _, p_input_depth[c1][c2] = functions.p_values(depth, 'depth', m, c1, c2, 'measure')

    # plotting p-value tables
    functions.tablesubplot(ax4[0][Measures.index(m)], p_grab_fails, '{} Failed Grabs'.format(m))
    functions.tablesubplot(ax4[1][Measures.index(m)], p_grab_succes, '{} Correct grabs'.format(m))
    functions.tablesubplot(ax4[2][Measures.index(m)], p_grab_attemts, '{} Grab attempts'.format(m))
    functions.tablesubplot(ax4[3][Measures.index(m)], p_input_velocity, '{} Grab Velocity'.format(m))
    functions.tablesubplot(ax4[4][Measures.index(m)], p_input_depth, '{} Input depth'.format(m))
    
fig4.tight_layout()
fig4.savefig("plots/p_values_trials.jpg".format(m))

#%% calculating p_values for trial 1-3 learning effects
print(), print('Calculating P-value tables for learning effects')
fig5, ax5 = plt.subplots(5, 3, figsize=(9, 10))
fig5.patch.set_visible(False)

for t in Trials:
    print("Trial: {}".format(t))
    
    p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_succes = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_input_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_input_depth = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

    for c1 in Conditions[1:]:
        for c2 in Conditions[1:]:

            _, p_grab_fails[c1][c2] = functions.p_values(trial_grabs, 'fails', t, c1, c2, 'trial')
            _, p_grab_succes[c1][c2] = functions.p_values(trial_grabs, 'succes', t, c1, c2, 'trial')
            _, p_grab_attemts[c1][c2] = functions.p_values(trial_grabs, 'attempts', t, c1, c2, 'trial')
            _, p_input_velocity[c1][c2] = functions.p_values(trial_velocity, 'velocity', t, c1, c2, 'trial')
            _, p_input_depth[c1][c2] = functions.p_values(trail_depth, 'depth', t, c1, c2, 'trial')

    # plotting p-value tables
    functions.tablesubplot(ax5[0][t-1], p_grab_fails, 'Failed Grabs Trial {}'.format(t))
    functions.tablesubplot(ax5[1][t-1], p_grab_succes, 'Correct grabs Trial {}'.format(t))
    functions.tablesubplot(ax5[2][t-1], p_grab_attemts, 'Grab attempts Trial {}'.format(t))
    functions.tablesubplot(ax5[3][t-1], p_input_velocity, 'Grab Velocity Trial {}'.format(t))
    functions.tablesubplot(ax5[4][t-1], p_input_depth, 'Input depth Trial {}'.format(t))

fig5.tight_layout()
fig5.savefig("plots/p_values_learning.jpg".format(t))

#%% saving variables
print(), print('Dumping evaluated data to file...')
dill.dump_session('data_evaluated.pkl')

end =  time.time()
print("Evaluation time: {}".format(end-start))