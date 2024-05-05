#!/usr/bin/env python3
# coding: utf-8
import sys
import matplotlib.pyplot as pyplot
import numpy as np
from scipy.signal import savgol_filter

#icm20984-accel is on 7,8,9 indexes.
accelStartIndex = 7
#icm20984-gyro is on 10,11,12 indexes.
gyroStartIndex = 10
#icm20984-magn is on 13,14,15 indexes.
magnStartIndex = 13
factor = 0.6072237558389597 # factor got from "andromeda-stationary.py"
accelName = "icm20984"

#data = np.genfromtxt("samples/rocket-flight.csv", delimiter=" ", skip_header=1)
data = np.genfromtxt("samples/rocket.csv", delimiter=" ", skip_header=1)
timestamp = data[:, 21].astype(int)

liftoffTs = 1919327
startTsIndex = np.where(timestamp == liftoffTs)[0][0] - 1
endTsIndex = np.size(timestamp) - 1

try:
    if sys.argv[1] == "accel2":
        #icm20600 is on 16,17,18 indexes.
        accelStartIndex = 16
        factor = 0.010232154063793143
        accelName = "icm20600"
    elif sys.argv[1] == "stationnary":
        startTsIndex = 0
        endTsIndex = np.where(timestamp == liftoffTs)[0][0] - 1
except:
    pass

print("ANDRONAV: parsing accel {} data (idx:{}) using factor {}"
      .format(accelName, accelStartIndex, factor))

#Parsing
accelEndIndex = accelStartIndex + 3
gyroEndIndex = gyroStartIndex + 3
magnEndIndex = magnStartIndex + 3
accelerometer = data[:,accelStartIndex:accelEndIndex]
gyro = data[:,gyroStartIndex:gyroEndIndex]
magn = data[:,magnStartIndex:magnEndIndex]

#Correcting
realAccel = accelerometer * factor
realGyro = gyro
realMagn = magn

flightAccel=realAccel[startTsIndex:endTsIndex]
flightGyro=realGyro[startTsIndex:endTsIndex]
flightMagn=realMagn[startTsIndex:endTsIndex]
flightTimestamp=timestamp[startTsIndex:endTsIndex]

absFlightAccel = np.sqrt(np.square(flightAccel[:, 0]) + np.square(flightAccel[:, 1]) + np.square(flightAccel[:, 2]))

#Smoothing
#smoothAbsFlightAccel = savgol_filter(absFlightAccel, 51, 3)

#Plotting
num_axes = 3 # we will plot 'num_axes' subplots
figure, axes = pyplot.subplots(nrows=num_axes, sharex=True)
figure.suptitle("Accel {} Analysis".format(accelName))
index_axe = 0

#axes[index_axe].plot(flightTimestamp, smoothAbsFlightAccel, "tab:blue", label="SMOOTHABSFLIGHTACC")
#axes[index_axe].plot(flightTimestamp, absFlightAccel, "tab:red", label="ABSFLIGHTACC")
#axes[index_axe].set_ylabel("Abs Flight Accel")
#axes[index_axe].grid()
#axes[index_axe].legend()
#index_axe += 1
#
axes[index_axe].plot(flightTimestamp, flightAccel[:, 0], "tab:red", label="FLIGHTACCX")
axes[index_axe].plot(flightTimestamp, flightAccel[:, 1], "tab:green", label="FLIGHTACCY")
axes[index_axe].plot(flightTimestamp, flightAccel[:, 2], "tab:blue", label="FLIGHTACCZ")
axes[index_axe].set_ylabel("Flight Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

axes[index_axe].plot(flightTimestamp, flightGyro[:, 0], "tab:red", label="FLIGHTGYROX")
axes[index_axe].plot(flightTimestamp, flightGyro[:, 1], "tab:green", label="FLIGHTGYROY")
axes[index_axe].plot(flightTimestamp, flightGyro[:, 2], "tab:blue", label="FLIGHTGYROZ")
axes[index_axe].set_ylabel("Flight Gyro")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

axes[index_axe].plot(flightTimestamp, flightMagn[:, 0], "tab:red", label="FLIGHTMAGNX")
axes[index_axe].plot(flightTimestamp, flightMagn[:, 1], "tab:green", label="FLIGHTMAGNY")
axes[index_axe].plot(flightTimestamp, flightMagn[:, 2], "tab:blue", label="FLIGHTMAGNZ")
axes[index_axe].set_ylabel("Flight Magn")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

pyplot.show()
