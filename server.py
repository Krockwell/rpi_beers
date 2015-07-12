#!/usr/bin/env python

import web
import thermometer

urls = ('/(.*)/', 'redirect', '/','index')

class redirect:
	def GET(self, path):
		web.seeother('/' + path)

class index:

	def __init__(self):
		self.hello = "Hey mans"

	def GET(self):
		current_temp_f = thermometer.read_temp()[1]
		out_string = "Current temperature is: " + str(current_temp_f) + " F"
		return out_string

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
		
