#!/usr/bin/env python
import os
import sys
import glob
from time import sleep
import RPi.GPIO as GPIO
import datetime
import logging
import logging.handlers


#Initialize temperature probes
#returns count and list of probe locations in filesystem
def init_probe():
	device_files = []
	probe_count = 0

	#load kenel module for temp probes
	os.system('/sbin/modprobe w1-gpio')
	os.system('/sbin/modprobe w1-therm')

	#Find each of the probes and add to list
	device_folders = glob.glob('/sys/bus/w1/devices/' + '28*')
	for folder in device_folders:
		probe_count += 1
		device_files.append(folder + '/w1_slave')
	print('Probe Init Complete')
	return device_files, probe_count


#reads temperature from device file 
def read_file(device_file):
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

#reads temperature, provides real temp values
def read_temp(device_file_list, number):
	lines = read_file(device_file_list[number])
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_file()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f

#Setup the Logger
def init_logger(probe_count):
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
	print('Probe Init complete', int(probe_number))
	return logger

def init_relay():
	GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(2, GPIO.OUT)
	print('Relay Init complete')
        return

def turn_on_relay():
        GPIO.output(2, GPIO.HIGH)
	print('turn on')
        return

def turn_off_relay():
        GPIO.output(2, GPIO.LOW)
	print('turn off')
        return


def generate_calendar(set_points):
	#Create a schedule given current date/time and provided steps           
        next_time_step = datetime.datetime.now()
        calendar = {}
        for lines in set_points:
                temp_step, time_step = lines.rstrip('\n').split(',')
                next_time_step = next_time_step + datetime.timedelta(days=int(time_step))

                #create a calendar, assumes only one temp change per day
		calendar[next_time_step.strftime("%d %b %Y ")] = [temp_step] 
	return calendar

#----Main---
#TODO:
#1. Need to hook this up to cherrypy
#2. calendar resets when program is re-run, needs to be more static
#2a.Input file -> intermediate generated calendar file -> loaded by default into program
#2b.IF program is run with no input file/argument, the current calendar is used

def main():
		
	#Assumes arguments are written properly
	if len(sys.argv) > 1:
		set_points = read_file(sys.argv[1])
		calendar = generate_calendar(set_points)
	else:
		print("No setpoints given")
		
	#Initialize temperature probes
	device_file_list,probe_count = init_probe()

	#Initialize telemetry logger
	logger = init_logger(probe_count)

	#Writes the temperature to a file
	#if the temperature is higher than the setpoint, turn on the fridge
	set_point = 68
	last_turn_on = datetime.datetime.now()
	relay_status = 0
	init_relay()
	i = 0
	while True:
		sleep(30)
		current_temp = read_temp(device_file_list, 0)[1]
		current_time = datetime.datetime.now()
		current_date = current_time.strftime("%d %b %Y ")

		#Use calendar to get new set_point
		if current_date in calendar:
			set_point = calendar[current_date]
					
		if current_temp > set_point:
			#Turn on after waiting for compressor delay
			if current_time - last_turn_on > datetime.timedelta(minutes=10):
				turn_on_relay()
				relay_status = 1
				last_turn_on = datetime.datetime.now()
		elif current_temp < set_point - 2 :
			relay_status = 0
			turn_off_relay()
		for probe_number in range(probe_count):
			logger[0].info('%f %d', current_temp, relay_status)
		

if __name__ == "__main__":
	main()
