# coding: utf-8
import matplotlib.pyplot as pyplot
import numpy
import sys

#Parsing
data = np.genfromtxt("samples/rocket-stationary.csv", delimiter=" ", skip_header=1)
accelerometer = data[:,7:10]
timestamp = (data[:, 21])/1000

#Analysis
# ...

#Plotting
num_axes = 2
index_axe = 0

figure, axes = pyplot.subplots(nrows=num_axes, sharex=True)
figure.suptitle("Accel analysis")

axes[index_axe].plot(timestamp, accelerometer[:, 0], "tab:red", label="Acc X")
axes[index_axe].plot(timestamp, accelerometer[:, 1], "tab:green", label="Acc Y")
axes[index_axe].plot(timestamp, accelerometer[:, 2], "tab:blue", label="Acc Z")
axes[index_axe].set_ylabel("Raw Accel")
axes[index_axe].grid()
axes[index_axe].legend()
index_axe += 1

pyplot.show()
