setup env: ./setup.sh
activate env: source .env/bin/activate
============================

telemetry data: samples/rocket.csv
frequency acquisition: 10Hz
imu data spec:
	chip: icm20984
	data: accel+gyro+magn
	config: ±16g/±500dps/±4900uT
	hardware sampling rate: 10Hz
	others: FIFO and DLP filter enabled but DMP mode is failing to be enabled.
imu2 data spec
	chip: icm20600
	data: accel2 (gyro was stored in sdcard)
	config: ±16g/±2000dps
	hardware sampling rate: ??Hz
	others: FIFO disabled.
	

