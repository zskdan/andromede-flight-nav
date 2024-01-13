#!/usr/bin/env python3
# coding: utf-8
import matplotlib.pyplot as pyplot
import numpy as np
import sys

#Parsing
data = np.genfromtxt("samples/rocket.csv", delimiter=" ", skip_header=1)
accelerometer = data[:,7:10]
timestamp = (data[:, 21])/1000

