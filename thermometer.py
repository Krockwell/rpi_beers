#!/usr/bin/env python
import os
import glob
from time import sleep
import RPi.GPIO as GPIO
import datetime
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

#reads temperature from a provided probe number
def read_temp_raw(number):
	f = open(device_files[number], 'r')
	lines = f.readlines()
	f.close()
	return lines

#reads temperature, provides real temp values
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
	
	probe_filename = 'Fermenter_Website/logs/temperature_p' + str(probe_number + 1) + '.log'
	console_handler.append(logging.FileHandler(filename=probe_filename,mode='a'))
	console_handler[probe_number].setLevel(logging.DEBUG)
	console_handler[probe_number].setFormatter(formatter)

for probe_number in range(probe_count):
	logger[probe_number].addHandler(console_handler[probe_number])


def init_relay():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2, GPIO.OUT)
	print('initializing')
        return

def turn_on_relay():
        GPIO.output(2, GPIO.HIGH)
	print('turn on')
        return

def turn_off_relay():
        GPIO.output(2, GPIO.LOW)
	print('turn off')
        return


#Writes the temperature to a file
#if the temperature is higher than the setpoint, turn on the fridge
set_point = 68
last_turn_on = datetime.datetime.now()
relay_status = 0
init_relay()
while True:
	sleep(30)	
	current_temp = read_temp(probe_number)[1]
	current_time = datetime.datetime.now()
	print(current_temp, current_time, relay_status)
	if current_temp > set_point:
		#Turn on after waiting for compressor delay
		if current_time - last_turn_on > datetime.timedelta(minutes=10):
			turn_on_relay()
			relay_status = 1
			print(current_temp, current_time, relay_status)
			last_turn_on = datetime.datetime.now()
	else:
		relay_status = 0
		print(current_temp, current_time, relay_status)
		turn_off_relay()
	for probe_number in range(probe_count):
		logger[probe_number].info('%f %d', current_temp, relay_status)
		

