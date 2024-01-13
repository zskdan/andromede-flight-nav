import imufusion
import matplotlib.pyplot as pyplot
import numpy
import sys

# Import sensor data
data = numpy.genfromtxt("/archive/andromede/analyze/samples/rocket-stationary.csv", delimiter=" ", skip_header=1)
tsstart = 544927

sample_rate = 10  # 10 Hz
margin = int(0.1 * sample_rate)  # 1 s

timestamp = (data[:, 21] - tsstart)/1000
accelerometer = data[:,7:10] * 60/1000
gyroscope = data[:, 10:13] / 3752.873558
magnetometer = data[:, 13:16] * 0.15
accel2 = data[:, 16:19] / 1000

# Instantiate algorithms
offset = imufusion.Offset(sample_rate)
ahrs = imufusion.Ahrs()

ahrs.settings = imufusion.Settings(imufusion.CONVENTION_NWU,  # convention
                                   0.5,  # gain
                                   10,  # acceleration rejection
                                   20,  # magnetic rejection
                                   5 * sample_rate)  # rejection timeout = 5 seconds

# Process sensor data
delta_time = numpy.diff(timestamp, prepend=timestamp[0])

euler = numpy.empty((len(timestamp), 3))
internal_states = numpy.empty((len(timestamp), 6))
flags = numpy.empty((len(timestamp), 5))
acceleration = numpy.empty((len(timestamp), 3))
is_moving = numpy.empty(len(timestamp))

for index in range(len(timestamp)):
    gyroscope[index] = offset.update(gyroscope[index])

    ahrs.update(gyroscope[index], accelerometer[index], magnetometer[index], delta_time[index])

    euler[index] = ahrs.quaternion.to_euler()

    ahrs_internal_states = ahrs.internal_states
    internal_states[index] = numpy.array([ahrs_internal_states.acceleration_error,
                                          ahrs_internal_states.accelerometer_ignored,
                                          ahrs_internal_states.acceleration_rejection_timer,
                                          ahrs_internal_states.magnetic_error,
                                          ahrs_internal_states.magnetometer_ignored,
                                          ahrs_internal_states.magnetic_rejection_timer])

    ahrs_flags = ahrs.flags
    flags[index] = numpy.array([ahrs_flags.initialising,
                                ahrs_flags.acceleration_rejection_warning,
                                ahrs_flags.acceleration_rejection_timeout,
                                ahrs_flags.magnetic_rejection_warning,
                                ahrs_flags.magnetic_rejection_timeout])

    acceleration[index] = 9.81 * ahrs.earth_acceleration  # convert g to m/s/s


######################################################
######################################################
######################################################
######################################################
######################################################
######################################################

for index in range(len(timestamp)):
    is_moving[index] = any(is_moving[index:(index + margin)])  # add leading margin

for index in range(len(timestamp) - 1, margin, -1):
    is_moving[index] = any(is_moving[(index - margin):index])  # add trailing margin

# Calculate velocity (includes integral drift)
velocity = numpy.zeros((len(timestamp), 3))

for index in range(len(timestamp)):
    if is_moving[index]:  # only integrate if moving
        velocity[index] = velocity[index - 1] + delta_time[index] * acceleration[index]

# Find start and stop indices of each moving period
is_moving_diff = numpy.diff(is_moving, append=is_moving[-1])

class IsMovingPeriod:
    start_index: int = -1
    stop_index: int = -1


is_moving_periods = []
is_moving_period = IsMovingPeriod()

for index in range(len(timestamp)):
    if is_moving_period.start_index == -1:
        if is_moving_diff[index] == 1:
            is_moving_period.start_index = index

    elif is_moving_period.stop_index == -1:
        if is_moving_diff[index] == -1:
            is_moving_period.stop_index = index
            is_moving_periods.append(is_moving_period)
            is_moving_period = IsMovingPeriod()

# Remove integral drift from velocity
velocity_drift = numpy.zeros((len(timestamp), 3))

for is_moving_period in is_moving_periods:
    start_index = is_moving_period.start_index
    stop_index = is_moving_period.stop_index

    t = [timestamp[start_index], timestamp[stop_index]]
    x = [velocity[start_index, 0], velocity[stop_index, 0]]
    y = [velocity[start_index, 1], velocity[stop_index, 1]]
    z = [velocity[start_index, 2], velocity[stop_index, 2]]

    t_new = timestamp[start_index:(stop_index + 1)]

    velocity_drift[start_index:(stop_index + 1), 0] = interp1d(t, x)(t_new)
    velocity_drift[start_index:(stop_index + 1), 1] = interp1d(t, y)(t_new)
    velocity_drift[start_index:(stop_index + 1), 2] = interp1d(t, z)(t_new)

velocity = velocity - velocity_drift

# Calculate position
position = numpy.zeros((len(timestamp), 3))

for index in range(len(timestamp)):
    position[index] = position[index - 1] + delta_time[index] * velocity[index]


print("Error: " + "{:.3f}".format(numpy.sqrt(position[-1].dot(position[-1]))) + " m")

######################################################
######################################################
######################################################
######################################################
######################################################
######################################################

def plot_bool(axis, x, y, label):
    axis.plot(x, y, "tab:cyan", label=label)
    pyplot.sca(axis)
    pyplot.yticks([0, 1], ["False", "True"])
    axis.grid()
    axis.legend()


#num_axes = 13
#ratios = [6, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 6]

#num_axes = 12
#ratios = [6, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1]
# Plot Euler angles
#figure, axes = pyplot.subplots(nrows=num_axes, sharex=True, gridspec_kw={"height_ratios": ratios})

num_axes = 2
figure, axes = pyplot.subplots(nrows=num_axes, sharex=True)
figure.suptitle("Euler angles, internal states, and flags")

index_axe = 0

if num_axes > index_axe:
    print("PLOP:"+str(index_axe))
    axes[index_axe].plot(timestamp, euler[:, 0], "tab:red", label="Roll")
    axes[index_axe].plot(timestamp, euler[:, 1], "tab:green", label="Pitch")
    axes[index_axe].plot(timestamp, euler[:, 2], "tab:blue", label="Yaw")
    axes[index_axe].set_ylabel("Degrees")
    axes[index_axe].grid()
    axes[index_axe].legend()
    index_axe += 1

# Plot initialising flag
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    plot_bool(axes[index_axe], timestamp, flags[:, 0], "Initialising")
#    index_axe += 1
#
## Plot acceleration rejection internal states and flags
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    axes[index_axe].plot(timestamp, internal_states[:, 0], "tab:olive", label="Acceleration error")
#    axes[index_axe].set_ylabel("Degrees")
#    axes[index_axe].grid()
#    axes[index_axe].legend()
#    index_axe += 1
#
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    plot_bool(axes[index_axe], timestamp, internal_states[:, 1], "Accelerometer ignored")
#    index_axe += 1
#
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    axes[index_axe].plot(timestamp, internal_states[:, 2], "tab:orange", label="Acceleration rejection timer")
#    axes[index_axe].grid()
#    axes[index_axe].legend()
#    index_axe += 1
#
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    plot_bool(axes[index_axe], timestamp, flags[:, 1], "Acceleration rejection warning")
#    index_axe += 1
#    plot_bool(axes[index_axe], timestamp, flags[:, 2], "Acceleration rejection timeout")
#    index_axe += 1
#
## Plot magnetic rejection internal states and flags
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    axes[index_axe].plot(timestamp, internal_states[:, 3], "tab:olive", label="Magnetic error")
#    axes[index_axe].set_ylabel("Degrees")
#    axes[index_axe].grid()
#    axes[index_axe].legend()
#    index_axe += 1
#
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    plot_bool(axes[index_axe], timestamp, internal_states[:, 4], "Magnetometer ignored")
#    index_axe += 1
#
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    axes[index_axe].plot(timestamp, internal_states[:, 5], "tab:orange", label="Magnetic rejection timer")
#    axes[index_axe].grid()
#    axes[index_axe].legend()
#    index_axe += 1
#
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    plot_bool(axes[index_axe], timestamp, flags[:, 3], "Magnetic rejection warning")
#    index_axe += 1
#
#if num_axes > index_axe:
#    print("PLOP:"+str(index_axe))
#    plot_bool(axes[index_axe], timestamp, flags[:, 4], "Magnetic rejection timeout")
#    index_axe += 1
#
if num_axes > index_axe:
    print("PLOP:"+str(index_axe))
    axes[index_axe].plot(timestamp, acceleration[:, 0], "tab:red", label="X")
    axes[index_axe].plot(timestamp, acceleration[:, 1], "tab:green", label="Y")
    axes[index_axe].plot(timestamp, acceleration[:, 2], "tab:blue", label="Z")
    axes[index_axe].set_ylabel("Acceleration")
    axes[index_axe].grid()
    axes[index_axe].legend()
    index_axe += 1


# Plot velocity
if num_axes > index_axe:
    print("PLOP:"+str(index_axe))
    axes[index_axe].plot(timestamp, velocity[:, 0], "tab:red", label="X")
    axes[index_axe].plot(timestamp, velocity[:, 1], "tab:green", label="Y")
    axes[index_axe].plot(timestamp, velocity[:, 2], "tab:blue", label="Z")
    axes[index_axe].set_ylabel("Velocity")
    axes[index_axe].grid()
    axes[index_axe].legend()
    index_axe += 1

# Plot position
if num_axes > index_axe:
    print("PLOP:"+str(index_axe))
    axes[index_axe].plot(timestamp, position[:, 0], "tab:red", label="X")
    axes[index_axe].plot(timestamp, position[:, 1], "tab:green", label="Y")
    axes[index_axe].plot(timestamp, position[:, 2], "tab:blue", label="Z")
    axes[index_axe].set_ylabel("Position")
    axes[index_axe].grid()
    axes[index_axe].legend()
    index_axe += 1

if len(sys.argv) == 1:  # don't show plots when script run by CI
    pyplot.show()
