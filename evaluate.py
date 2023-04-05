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

#%% calculating p_values for avg measures
print(), print('Calculating P-value tables for average data')

# fig4, ax4 = plt.subplots(7, 4, figsize=(12, 14))
# fig4.patch.set_visible(False)
p_grab_fails = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_grab_succes = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
p_grab_attemts = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
for c1 in Conditions[1:]:
    for c2 in Conditions[1:]:

        _, p_grab_fails[c1][c2] = functions.p_values(grabs, 'count', 'fails', c1, c2, 'measure')
        _, p_grab_succes[c1][c2] = functions.p_values(grabs, 'count', 'succes', c1, c2, 'measure')
        _, p_grab_attemts[c1][c2] = functions.p_values(grabs, 'count', 'attempts', c1, c2, 'measure')

for m in Measures:  
    p_pre_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_post_velocity = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_hmd_movement = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_correlation = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_force = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])
    p_count_avg = pd.DataFrame(index = Conditions[1:], columns = Conditions[1:])

    for c1 in Conditions[1:]:
        for c2 in Conditions[1:]:
            _, p_pre_velocity[c1][c2] = functions.p_values(velocity, 'value', 'pre', c1, c2, 'measure')
            _, p_post_velocity[c1][c2] = functions.p_values(velocity, 'value', 'post', c1, c2, 'measure')
            if c1 != 'B' and c2 != 'B':
                _, p_hmd_movement[c1][c2] = functions.p_values(hmd_movement, 'std', m, c1, c2, 'measure')
            _, p_correlation[c1][c2] = functions.p_values(in_out_corr, 'corr', m, c1, c2, 'measure')
            _, p_force[c1][c2] = functions.p_values(force, 'force', m, c1, c2, 'measure')
            
            diff_c1 = count_avg[(count_avg['condition']==c1)]['blocks']
            diff_c2 = count_avg[(count_avg['condition']==c2)]['blocks']
            p_value = np.round(stats.ttest_rel(diff_c1, diff_c2, nan_policy='omit') , 3)
            p_count_avg[c1][c2] = p_value[1]

    # plotting p-value tables
    functions.tablesubplot(ax2[1,0], p_grab_attemts, 'Grab attempts paired T-test p-values')
    functions.tablesubplot(ax2[1,1], p_grab_fails, 'Failed Grabs paired T-test p-values')
    functions.tablesubplot(ax2[2,0], p_grab_succes, 'Succesful grabs paired T-test p-values')
    functions.tablesubplot(ax2[2,1], p_count_avg, 'Blocks transferred paired T-test p-values')
    functions.tablesubplot(ax2[4,0], p_pre_velocity, 'Pre-Grab Velocity paired T-test p-values')
    functions.tablesubplot(ax2[4,1], p_post_velocity, 'Post-Grab Velocity paired T-test p-values')
    functions.tablesubplot(ax2[5,1], p_hmd_movement, 'HMD rotational SD paired T-test p-values')
    functions.tablesubplot(ax2[6,1], p_correlation, 'Input-Output Correlation paired T-test p-values')
    functions.tablesubplot(ax2[7,1], p_force, 'Average peak force paired T-test p-values')

    
fig2.tight_layout()
fig2.savefig("plots/average_results.jpg", dpi=1000)
fig2.savefig("plots/average_results.svg", dpi=1000)

#%% saving variables
print(), print('Dumping evaluated data to file...')
dill.dump_session('data_evaluated.pkl')

end =  time.time()
print("Evaluation time: {}".format(end-evaluate_start))