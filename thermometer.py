#!/usr/bin/env python
import os
import glob
import time
import logging
import logging.handlers


os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

device_files = []
probe_count = 0

device_folders = glob.glob(base_dir + '28*')
for folder in device_folders:
	probe_count += 1
	device_files.append(folder + '/w1_slave')


def __init__(self):
	self.hello = "hey duuude"

def read_temp_raw(number):
	f = open(device_files[number], 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(number):
	lines = read_temp_raw(number)

	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f

#Setup the Logger
logger = []
console_handler = []

formatter = logging.Formatter('%(asctime)s %(message)s', "%Y-%m-%d %H:%M:%S")

for probe_number in range(probe_count):
	logger.append(logging.getLogger('Probe' + str(probe_number)))
	logger[probe_number].setLevel(logging.DEBUG)
	
	probe_filename = 'logs/temperature_p' + str(probe_number + 1) + '.log'
	console_handler.append(logging.FileHandler(filename=probe_filename,mode='a'))
	console_handler[probe_number].setLevel(logging.DEBUG)
	console_handler[probe_number].setFormatter(formatter)

for probe_number in range(probe_count):
	logger[probe_number].addHandler(console_handler[probe_number])


#Writes the temperature to a file every 60 seconds
while True:
	for probe_number in range(probe_count):
		logger[probe_number].info('%f', read_temp(probe_number)[1])
	time.sleep(60)

