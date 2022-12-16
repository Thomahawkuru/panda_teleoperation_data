#%% import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.express as px
import dill

dill.load_session('data_calculated.pkl')

#%% plot sanity check data    
fpss = []
times = []

for c in Participants:
    for c in Conditions[1:]:
        for t in Trials:
            fpss.append(data[p][c][t]['fps'])
            times.append(data[p][c][t]['duration'])        

fig1, ax1 = plt.subplots()
ax1.boxplot([fpss,times])
ax1.set_title('Sanity Checking, n = [{}]'.format(2*5*3))
ax1.set_xticklabels(['Average FPS','Duration'])
fig1.savefig("plots/sanity_check.jpg")

#%% plot grab data
average_velocity = pd.DataFrame()
failed_grabs = pd.DataFrame()
correct_grabs = pd.DataFrame()

for c in Conditions[1:]:
    velocity = []
    fails = []
    succes = []
    for p in Participants:
        vel = 0
        failed = 0
        correct = 0
        for t in Trials:
            vel += np.mean(data[p][c][t]['velocity'])
            failed += data[p][c][t]['grabs']['fail']
            correct += data[p][c][t]['grabs']['succes']
        
        velocity.append(vel/3)
        fails.append(failed/3)
        succes.append(correct/3)

    average_velocity[c] = velocity
    failed_grabs[c] = fails
    correct_grabs[c] = succes

fig2, ax2 = plt.subplots()
ax2.boxplot(average_velocity)
ax2.set_title('Average Velocity [m/s]')
ax2.set_xlabel('Conditions')
ax2.set_xticklabels(['B','C','D','E','F'])
fig2.savefig("plots/average_velocity.jpg")

fig3, ax3 = plt.subplots()
ax3.boxplot(correct_grabs)
ax3.set_title('Correct Grabs [Average n]')
ax3.set_xticklabels(['B','C','D','E','F'])
ax3.set_xlabel('Conditions')
fig3.savefig("plots/correct_grabs.jpg")

fig4, ax4 = plt.subplots()
ax4.boxplot(failed_grabs)
ax4.set_title('Failed Grabs [Average n]')
ax4.set_xlabel('Conditions')
ax4.set_xticklabels(['B','C','D','E','F'])
fig4.savefig("plots/failed_grabs.jpg")

#%% plot input paths
# for p in Participants:
#     for c in Conditions[1:]:
#         for t in Trials:
#             plt.plot(data[p][c][t]['Hand'].posZ) 
#             fig3 = px.line_3d(data[p][c][t]['Hand'], x='posZ', y='posX', z='posY', title = 'Hand input')
#             plot(fig3, filename='plots/fig{}{}{}.html'.format(p,c,t,))

# %%
print(), print('Dumping plotted data to file...')
dill.dump_session('data_plotted.pkl')