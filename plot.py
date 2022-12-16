#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import dill
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

fig1, ax1 = plt.subplots()
ax1.boxplot([fpss,times,track_err])
ax1.set_title('Sanity Checking, n = [{}]'.format(2*5*3))
ax1.set_xticklabels(['Average FPS','Duration','Tracking errors'])
fig1.savefig("plots/sanity_check.jpg")

#%% plot data per condition
failed_grabs = pd.DataFrame()
correct_grabs = pd.DataFrame()
average_velocity = pd.DataFrame()

for c in Conditions[1:]:
    Fails = []
    Succes = []
    Velocity = []

    for p in Participants:
        failed = 0
        correct = 0
        velocity = 0

        for t in Trials:
            failed += data[p][c][t]['grabs']['fail']
            correct += data[p][c][t]['grabs']['succes']
            velocity += np.mean(data[p][c][t]['velocity'])

        
        Velocity.append(velocity/3)
        Fails.append(failed/3)
        Succes.append(correct/3)

    failed_grabs[c] = Fails
    correct_grabs[c] = Succes
    average_velocity[c] = Velocity

fig2, ax2 = plt.subplots()
ax2.boxplot(failed_grabs)
ax2.set_title('Failed Grabs [Average n]')
ax2.set_xlabel('Conditions')
ax2.set_xticklabels(['B','C','D','E','F'])
fig2.savefig("plots/failed_grabs.jpg")

fig3, ax3 = plt.subplots()
ax3.boxplot(correct_grabs)
ax3.set_title('Correct Grabs [Average n]')
ax3.set_xticklabels(['B','C','D','E','F'])
ax3.set_xlabel('Conditions')
fig3.savefig("plots/correct_grabs.jpg")

fig4, ax4 = plt.subplots()
ax4.boxplot(average_velocity)
ax4.set_title('Average Velocity [m/s]')
ax4.set_xlabel('Conditions')
ax4.set_xticklabels(['B','C','D','E','F'])
fig4.savefig("plots/average_velocity.jpg")

#%% plot input paths
# for p in Participants:
#     for c in Conditions[1:]:
#         for t in Trials:
#             plot_data = functions.crop_data(data[p][c][t]['Hand'][['posZ','posX','posY']],data[p][c][t]['Experiment'])
#             fig3 = px.line_3d(plot_data, x='posZ', y='posX', z='posY', title = 'Hand input')
#             plot(fig3, filename='plots/fig{}{}{}.html'.format(p,c,t,))

# %%
print(), print('Dumping plotted data to file...')
dill.dump_session('data_plotted.pkl')