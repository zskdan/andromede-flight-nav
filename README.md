setup env: ./setup.sh
activate env: source .env/bin/activate
============================

telemetry data: samples/rocket.csv
acquisition frequency: 10Hz
imu data spec:
	chip: icm20948
	data: accel+gyro+magn
	config: ±16g/±500dps/±4900uT
	hardware sampling rate: 10Hz
	others: FIFO enabled
		DLPF configured (acc_d11bw5_n17bw, gyr_d11bw6_n17bw8) but not enabled.
		DMP mode is failing to be enabled.
		Low Power mode disabled.

imu2 data spec
	chip: icm20600
	data: accel2 (gyro was stored in sdcard)
	config: ±16g/±2000dps
	hardware sampling rate: 1KHz (ODR)
	others: FIFO disabled
                DLPF enabled (Rate:1Khz + 3db-BW/gyro:176Hz 3db-BW/accel:420Hz)
		Low Power mode enable (averaging Gyro:x1 accel:x4) 

notes:

icm20600 has 2 modes:
	Low Noise mode:
	Low Power mode:
		1. (6axis) is the one configured by with high 4KHz rate instead of ODR of 10Hz (SMPLRT_DIV) 
		2. The low-power mode of operation, the accelerometer is duty-cycled

icm20980 has a runtime calibration firmware.

ODR: output data rate
DMP: digital motion processor can be used to offload computations
DLPF: on-board Digital Low Pass Filter(uselly to remove noise from the data).

