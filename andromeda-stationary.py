#!/usr/bin/env python3
# coding: utf-8
import matplotlib.pyplot as pyplot
import pandas as pd
import numpy as np
from scipy import stats
import sys

#icm20984 on 7,8,9 indexes.
accelStartIndex = 7
#icm20600 on 16,17,18 indexes.
#accelStartIndex = 16
accelEndIndex = accelStartIndex + 3

#Parsing
data = np.genfromtxt("samples/rocket-stationary.csv", delimiter=" ", skip_header=1)
accelerometer = data[:,accelStartIndex:accelEndIndex]
timestamp = (data[:, 21])/1000

#Analysis

## define the absolth acceleration sqrt(x2+y2+z2)
absAccel = np.sqrt(np.square(accelerometer[:, 0]) + np.square(accelerometer[:, 1]) + np.square(accelerometer[:, 2]))

# and add it in a pandas dataframe to remove outliers
df = pd.DataFrame({'absAccel': absAccel})

## calculate z-score to detect outliers
threshold = 0.2 # emperical value that match the overall value after making the rocket horizental.
z = np.abs(stats.zscore(df['absAccel']))
## replace the outliers
df.loc[z > threshold, 'absAccel'] = df['absAccel'].median()

median = df['absAccel'].median()
factor = 9.81/median

cleanAbsAccel = absAccel*factor
print('median is {}, thus factor is {}'.format(median, factor))

# now normalize the accelerometer data.
cleanAccel = accelerometer*factor

#Plotting
num_axes = 4 # we will plot 'num_axes' subplots
figure, axes = pyplot.subplots(nrows=num_axes, sharex=True)
figure.suptitle("Accel Stationary Analysis")
index_axe = 0

axes[index_axe].plot(timestamp, accelerometer[:, 0], "tab:red", label="RAWACCX")
axes[index_axe].plot(timestamp, accelerometer[:, 1], "tab:green", label="RAWACCY")
axes[index_axe].plot(timestamp, accelerometer[:, 2], "tab:blue", label="RAWACCZ")
axes[index_axe].set_ylabel("Raw Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

axes[index_axe].plot(timestamp, absAccel, "tab:red", label="ABS")
axes[index_axe].set_ylabel("Abs Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

axes[index_axe].plot(timestamp, cleanAbsAccel, "tab:red", label="CLEANABS")
axes[index_axe].set_ylabel("Clean Abs Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

axes[index_axe].plot(timestamp, cleanAccel[:, 0], "tab:red", label="CLEANACCX")
axes[index_axe].plot(timestamp, cleanAccel[:, 1], "tab:green", label="CLEANACCY")
axes[index_axe].plot(timestamp, cleanAccel[:, 2], "tab:blue", label="CLEANACCZ")
axes[index_axe].set_ylabel("Clean Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

pyplot.show()
