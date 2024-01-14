#!/usr/bin/env python3
# coding: utf-8
import matplotlib.pyplot as pyplot
import numpy as np
import sys

#icm20984 on 7,8,9 indexes.
accelStartIndex = 7
#icm20600 on 16,17,18 indexes.
#accelStartIndex = 16
accelEndIndex = accelStartIndex + 3

#Parsing
data = np.genfromtxt("samples/rocket.csv", delimiter=" ", skip_header=1)
accelerometer = data[:,accelStartIndex:accelEndIndex]
timestamp = (data[:, 21])/1000

factor = 0.6072237558389597 # calculated with "andromeda-stationary.py"
print("ANDRONAV: using factor {}".format(factor))

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
figure.suptitle("Accel Analysis")
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
