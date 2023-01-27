import pandas as pd
import numpy as np
import dill
from scipy import stats
import functions

dill.load_session('data_plotted.pkl')

#%% calculating p_values
print('Calculating P-value tables')

for m in Measures:
    print("Measure: {}".format(m))
    
    p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_succes = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_input_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_input_depth = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

    for c1 in Conditions[1:]:
        for c2 in Conditions[1:]:

            _, p_grab_fails[c1][c2] = functions.p_values(grab_fails, 'fails', m, c1, c2)
            _, p_grab_succes[c1][c2] = functions.p_values(grab_succes, 'succes', m, c1, c2)
            _, p_grab_attemts[c1][c2] = functions.p_values(grab_attempts, 'attempts', m, c1, c2)
            _, p_input_velocity[c1][c2] = functions.p_values(velocity, 'velocity', m, c1, c2)
            _, p_input_depth[c1][c2] = functions.p_values(depth, 'depth', m, c1, c2)

    # print('Failed grabs:'), print(p_grab_fails), print()
    # print('Correct grabs:'), print(p_grab_succes), print()
    # print('Grab attempts:'), print(p_grab_attemts), print()     
    # print('Input velocity:'), print(p_input_velocity), print()
    # print('Input Depth:'), print(p_input_depth), print()     

    print('Plotting P-value tables')

    #%% plotting p-value tables
    fig4, ax4 = plt.subplots(5, 1, figsize=(5, 10))
    fig4.patch.set_visible(False)

    functions.tablesubplot(ax4[0], p_grab_fails, '{} Failed Grabs'.format(m))
    functions.tablesubplot(ax4[1], p_grab_succes, '{} Correct grabs'.format(m))
    functions.tablesubplot(ax4[2], p_grab_attemts, '{} Grab attempts'.format(m))
    functions.tablesubplot(ax4[3], p_input_velocity, '{} Input Velocity'.format(m))
    functions.tablesubplot(ax4[4], p_input_depth, '{} Input depth'.format(m))
    fig4.tight_layout()
    fig4.savefig("plots/p_values_{}.jpg".format(m))

#%% saving variables
print(), print('Dumping evaluated data to file...')
dill.dump_session('data_evaluated.pkl')