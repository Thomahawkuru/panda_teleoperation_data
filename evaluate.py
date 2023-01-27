import pandas as pd
import numpy as np
import dill
import matplotlib.pyplot as plt
from scipy import stats
import functions

dill.load_session('data_plotted.pkl')

#%% calculating p_values for min/med/max/avg measures
print(), print('Calculating P-value tables over all trials')

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
    fig4, ax4 = plt.subplots(5, 1, figsize=(5, 10))
    fig4.patch.set_visible(False)

    functions.tablesubplot(ax4[0], p_grab_fails, '{} Failed Grabs'.format(m))
    functions.tablesubplot(ax4[1], p_grab_succes, '{} Correct grabs'.format(m))
    functions.tablesubplot(ax4[2], p_grab_attemts, '{} Grab attempts'.format(m))
    functions.tablesubplot(ax4[3], p_input_velocity, '{} Input Velocity'.format(m))
    functions.tablesubplot(ax4[4], p_input_depth, '{} Input depth'.format(m))
    
    fig4.tight_layout()
    fig4.savefig("plots/p_values_{}.jpg".format(m))

#%% calculating p_values for trial 1-3 learning effects
print(), print('Calculating P-value tables for learning effects')

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
    fig4, ax4 = plt.subplots(5, 1, figsize=(5, 10))
    fig4.patch.set_visible(False)

    functions.tablesubplot(ax4[0], p_grab_fails, 'Failed Grabs Trial {}'.format(t))
    functions.tablesubplot(ax4[1], p_grab_succes, 'Correct grabs Trial {}'.format(t))
    functions.tablesubplot(ax4[2], p_grab_attemts, 'Grab attempts Trial {}'.format(t))
    functions.tablesubplot(ax4[3], p_input_velocity, 'Input Velocity Trial {}'.format(t))
    functions.tablesubplot(ax4[4], p_input_depth, 'Input depth Trial {}'.format(t))
    
    fig4.tight_layout()
    fig4.savefig("plots/p_values_trial_{}.jpg".format(t))

#%% saving variables
print(), print('Dumping evaluated data to file...')
dill.dump_session('data_evaluated.pkl')