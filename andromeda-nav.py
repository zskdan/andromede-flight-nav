#!/usr/bin/env python3
# coding: utf-8
import matplotlib.pyplot as pyplot
import numpy as np
import sys

#Parsing
data = np.genfromtxt("samples/rocket.csv", delimiter=" ", skip_header=1)
accelerometer = data[:,7:10]
timestamp = (data[:, 21])/1000

factor = 0.6072237558389597 # calculated with "andromeda-stationary.py"
print("ANDRONAV: using factor {}".format(factor))

#Correcting
realAccel = accelerometer * factor
startts=1919327/1000
lastts=timestamp[-1]

#Plotting
num_axes = 2 # we will plot 'num_axes' subplots
figure, axes = pyplot.subplots(nrows=num_axes, sharex=True)
figure.suptitle("Accel Analysis")
index_axe = 0

axes[index_axe].plot(timestamp, accelerometer[:, 0], "tab:red", label="RAWACCX")
axes[index_axe].plot(timestamp, accelerometer[:, 1], "tab:green", label="RAWACCY")
axes[index_axe].plot(timestamp, accelerometer[:, 2], "tab:blue", label="RAWACCZ")
axes[index_axe].set_ylabel("Raw Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

axes[index_axe].plot(timestamp, realAccel[:, 0], "tab:red", label="REALACCX")
axes[index_axe].plot(timestamp, realAccel[:, 1], "tab:green", label="REALACCY")
axes[index_axe].plot(timestamp, realAccel[:, 2], "tab:blue", label="REALACCZ")
axes[index_axe].set_ylabel("Real Accel")
axes[index_axe].grid()
axes[index_axe].legend()
axes[index_axe].axvspan(startts, lastts, facecolor='yellow', alpha=0.5, hatch='/', edgecolor='red', linewidth=5)
index_axe += 1

pyplot.show()
