from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob

# Fixing random state for reproducibility
np.random.seed(2022)

S = 24 # number of samples /plot/user
N = 9 # number of users
focals = ['Center', 'North', 'South', 'East', 'West']*2
angle = np.repeat(['30', '60'], 5)
gt = np.arange(0, 360, 15)
fig = plt.figure()

# read data
raw_data = pd.read_csv('data/data.csv', header=None)

# read images
images = [plt.imread(file) for file in glob.glob("./hand_anno/*.jpg")]

# compute difference angle
def diff_angle(data):
    error = []
    for tar, src in zip(data, gt):
        diff = tar - src
        diff = (diff + 180) % 360 - 180
        error.append(abs(diff))
    # print('error: ', error)
    return error

def scatter(p, u, plot):
    # polar plot parameters
    data = raw_data.iloc[p*S:(p+1)*S,2*u].to_numpy()
    theta = [ang*2*np.pi/360 for ang in data]
    r = raw_data.iloc[p*S:(p+1)*S,2*u+1].to_numpy() * 0.2
    area = [20] * S
    err = diff_angle(data)
    plot.scatter(theta, r, c=err, s=area, cmap='binary', alpha=0.75, zorder=2)

def plot(n):
    for i in range(10):
        polar = fig.add_subplot(2,5,1+i, projection='polar')
        polar.set_rlim(0,1)
        polar.set_rticks(np.arange(0, 1, 0.2))
        polar.yaxis.set_tick_params(labelsize=6)
        polar.xaxis.set_tick_params(labelsize=8)
        # polar.set_yticklabels([])
        polar.set_xticks(np.arange(0,2.0*np.pi,np.pi/12.0))
        polar.set_theta_zero_location('S')
        polar.set_theta_direction(-1)
        polar.set_title(f'Focal: {focals[i]}; {angle[i]}°')
        img = polar.inset_axes([-0.4, 0.9, 0.5, 0.5], zorder=1)
        img.imshow(images[i%5])
        img.axis('off')
        
        # iterate through n users
        for j in range(n):
            scatter(i, j, polar) # the ith plot of the jth user

        # plot for single user
        # scatter(i, 5, polar) # the ith plot of the jth user

#  plot
fig.tight_layout()
fig.set_size_inches(15.36, 7.59)
plt.subplots_adjust(wspace=0.7, hspace=0)
plot(N)
plt.savefig('./results/9users.png')
# plt.show()