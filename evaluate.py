import pandas as pd
import numpy as np
import dill
from scipy import stats
import functions

dill.load_session('data_plotted.pkl')

print('Calculating P-value tables')

p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_grab_succes = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_input_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_input_depth = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

for c1 in Conditions[1:]:
    for c2 in Conditions[1:]:

        _, p_grab_fails[c1][c2] = np.round(stats.ttest_rel(failed_grabs[c1], failed_grabs[c2]),3)
        _, p_grab_succes[c1][c2] = np.round(stats.ttest_rel(correct_grabs[c1], correct_grabs[c2]) ,3)
        _, p_grab_attemts[c1][c2] = np.round(stats.ttest_rel(grab_attempts[c1], grab_attempts[c2]),3)
        _, p_input_velocity[c1][c2] = np.round(stats.ttest_rel(average_velocity[c1], average_velocity[c2]),3)
        _, p_input_depth[c1][c2] = np.round(stats.ttest_rel(input_depth[c1], input_depth[c2]),3)

print('Failed grabs:'), print(p_grab_fails), print()
print('Correct grabs:'), print(p_grab_succes), print()
print('Grab attempts:'), print(p_grab_attemts), print()     
print('Input velocity:'), print(p_input_velocity), print()
print('Input Depth:'), print(p_input_depth), print()     

print('Plotting P-value tables')

fig8, ax8 = plt.subplots(5, 1, figsize=(5, 10))

fig8.patch.set_visible(False)

functions.subplot(ax8[0], p_grab_fails, 'Failed Grabs')
functions.subplot(ax8[1], p_grab_succes, 'Correct grabs')
functions.subplot(ax8[2], p_grab_attemts, 'Grab attempts')
functions.subplot(ax8[3], p_input_velocity, 'Input Velocity')
functions.subplot(ax8[4], p_input_depth, 'Input depth')

fig8.tight_layout()
fig8.savefig("plots/p_values.jpg")


print(), print('Dumping evaluated data to file...')
dill.dump_session('data_evaluated.pkl')