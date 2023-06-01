#%%
import time
import pandas as pd
import numpy as np
import dill
import matplotlib.pyplot as plt
from scipy import stats
import functions

evaluate_start = time.time()
dill.load_session('data_plotted.pkl')

#%% Evaluation sanity check data
unvalid = pd.DataFrame([] , columns=['fps', 'duration', 'track_err'])
print(), print('Calculating P-value tables for sanity check data')

p_fps = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_duration = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_tracking_err = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_input_lag = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

for c1 in Conditions[1:]:
    for c2 in Conditions[1:]:
        _, p_fps[c1][c2] = functions.p_values(fpss, 'fps', None, c1, c2, None)
        _, p_duration[c1][c2] = functions.p_values(times, 'duration [s]', None, c1, c2, None)
        _, p_tracking_err[c1][c2] = functions.p_values(track_err, 'track_err', None, c1, c2, None)
        _, p_input_lag[c1][c2] = functions.p_values(input_lag, 'lag [s]', None, c1, c2, None)

functions.tablesubplot(ax1[0,1], p_fps, 'Grab attempts paired T-test p-values')
functions.tablesubplot(ax1[1,1], p_duration, 'Failed Grabs paired T-test p-values')
functions.tablesubplot(ax1[2,1], p_tracking_err, 'successful grabs paired T-test p-values')
functions.tablesubplot(ax1[3,1], p_input_lag, 'Blocks transferred paired T-test p-values')

fig1.tight_layout()
fig1.savefig("plots/sanity_check.jpg", dpi=1000)
fig1.savefig("plots/sanity_check.svg", dpi=1000)

#%% calculating p_values for avg measures
print(), print('Calculating P-value tables for average data')
p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_grab_success = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_count_avg = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

for c1 in Conditions[1:]:
    for c2 in Conditions[1:]:
        _, p_grab_fails[c1][c2] = functions.p_values(grabs, 'count', 'fails', c1, c2, 'measure')
        _, p_grab_success[c1][c2] = functions.p_values(grabs, 'count', 'success', c1, c2, 'measure')
        _, p_grab_attemts[c1][c2] = functions.p_values(grabs, 'count', 'attempts', c1, c2, 'measure')

p_pre_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_post_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_hmd_movement = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_force = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_hits = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:]) 
p_correlation = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

for c1 in Conditions[1:]:
    for c2 in Conditions[1:]:
        _, p_pre_velocity[c1][c2] = functions.p_values(velocity, 'velocity', 'pre', c1, c2, 'measure')
        _, p_post_velocity[c1][c2] = functions.p_values(velocity, 'velocity', 'post', c1, c2, 'measure')
        if c1 != 'B' and c2 != 'B':
            _, p_hmd_movement[c1][c2] = functions.p_values(hmd_movement, 'std', 'Head Movement', c1, c2, 'measure')
        _, p_force[c1][c2] = functions.p_values(force, 'force', 'Peak Force', c1, c2, 'measure')
        _, p_hits[c1][c2] = functions.p_values(hits, 'hits', 'Hits', c1, c2, 'measure')
        _, p_correlation[c1][c2] = functions.p_values(in_out_corr, 'corr', 'In-out Correlation', c1, c2, 'measure')
        
        diff_c1 = grabs['count'][grabs['condition']==c1][grabs['measure']=='transfer']
        diff_c2 = grabs['count'][grabs['condition']==c2][grabs['measure']=='transfer']
    
        p_value = np.round(stats.ttest_rel(diff_c1, diff_c2, nan_policy='omit') , 3)
        p_count_avg[c1][c2] = p_value[1]

#%% plotting p-value tables
fig3, ax3 = plt.subplots(5, 2, figsize=(7.5, 10))
functions.tablesubplot(ax3[0,0], p_grab_attemts, 'Grab attempts paired T-test p-values')
functions.tablesubplot(ax3[0,1], p_grab_fails, 'Failed Grabs paired T-test p-values')
functions.tablesubplot(ax3[1,0], p_grab_success, 'successful grabs paired T-test p-values')
functions.tablesubplot(ax3[1,1], p_count_avg, 'Blocks transferred paired T-test p-values')
functions.tablesubplot(ax3[2,0], p_pre_velocity, 'Pre-Grab Velocity paired T-test p-values')
functions.tablesubplot(ax3[2,1], p_post_velocity, 'Post-Grab Velocity paired T-test p-values')
functions.tablesubplot(ax3[3,0], p_hmd_movement, 'HMD Rotational SD paired T-test p-values')
functions.tablesubplot(ax3[3,1], p_force, 'Average peak force paired T-test p-values')
functions.tablesubplot(ax3[4,0], p_hits, 'number of hits paired T-test p-values')
functions.tablesubplot(ax3[4,1], p_correlation, 'Input-Output Correlation paired T-test p-values')
    
fig3.tight_layout()
fig3.savefig("plots/p_values_measures.jpg", dpi=1000)
fig3.savefig("plots/p_values_measures.svg", dpi=1000)

#%% saving variables
print(), print('Dumping evaluated data to file...')
dill.dump_session('data_evaluated.pkl')

end =  time.time()
print("Evaluation time: {}".format(end-evaluate_start))