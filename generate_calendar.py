#!/usr/bin/env python
import datetime
import sys
import json

def read_file(device_file):
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def generate_calendar(set_points):
	#Create a schedule given current date/time and provided steps           
        iter_date = datetime.datetime.now()
        calendar = {}
	total_days = 0
        for lines in set_points:
                temp_step, time_step = lines.rstrip('\n').split(',')
		for days in range(int(time_step)):
			calendar[iter_date.strftime("%d %b %Y ")] = temp_step
			iter_date = iter_date + datetime.timedelta(days=1)
			total_days += 1

        #Fill out an entire 30 day period
	if total_days < 30:
		for days in range(30 - total_days):
			calendar[iter_date.strftime("%d %b %Y ")] = temp_step
			iter_date = iter_date + datetime.timedelta(days=1)
	
	return calendar

def main():
	#Assumes arguments are written properly	
	#input file should written as temp,days
	if len(sys.argv) > 2:
		set_points = read_file(sys.argv[1])
		calendar = generate_calendar(set_points)
		with open(sys.argv[2], 'w') as json_file:
  			json.dump(calendar, json_file)		
	else:
		print("Missing setpoint file or output file")


if __name__ == "__main__":
	main()
