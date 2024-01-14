#!/usr/bin/env python3
# coding: utf-8
import matplotlib.pyplot as pyplot
import numpy as np
import sys
from scipy.signal import savgol_filter

#icm20984 is on 7,8,9 indexes.
accelStartIndex = 7
factor = 0.6072237558389597 # factor got from "andromeda-stationary.py"
accelName = "icm20984"

try:
    if sys.argv[1] == "accel2":
        #icm20600 is on 16,17,18 indexes.
        accelStartIndex = 16
        factor = 0.010232154063793143
        accelName = "icm20600"
except:
    pass

print("ANDRONAV: parsing accel {} data (idx:{}) using factor {}"
      .format(accelName, accelStartIndex, factor))

#Parsing
accelEndIndex = accelStartIndex + 3
data = np.genfromtxt("samples/rocket.csv", delimiter=" ", skip_header=1)
accelerometer = data[:,accelStartIndex:accelEndIndex]
timestamp = (data[:, 21])/1000

#Correcting
realAccel = accelerometer * factor

liftoffTs=1919327/1000
startTsIndex=np.where(timestamp == liftoffTs)[0][0] - 1

flightAccel=realAccel[startTsIndex:]
flightTimestamp=timestamp[startTsIndex:]

absFlightAccel = np.sqrt(np.square(flightAccel[:, 0]) + np.square(flightAccel[:, 1]) + np.square(flightAccel[:, 2]))

#Plotting
num_axes = 2 # we will plot 'num_axes' subplots
figure, axes = pyplot.subplots(nrows=num_axes, sharex=True)
figure.suptitle("Accel {} Analysis".format(accelName))
index_axe = 0

axes[index_axe].plot(flightTimestamp, absFlightAccel, "tab:red", label="ABSFLIGHTACC")
axes[index_axe].set_ylabel("Abs Flight Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

axes[index_axe].plot(flightTimestamp, flightAccel[:, 0], "tab:red", label="FLIGHTACCX")
axes[index_axe].plot(flightTimestamp, flightAccel[:, 1], "tab:green", label="FLIGHTACCY")
axes[index_axe].plot(flightTimestamp, flightAccel[:, 2], "tab:blue", label="FLIGHTACCZ")
axes[index_axe].set_ylabel("Flight Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

pyplot.show()
