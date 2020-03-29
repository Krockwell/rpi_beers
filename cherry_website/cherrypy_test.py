import os, os.path
import string
import cherrypy

class FermentationStation(object):
	@cherrypy.expose
	def index(self):
       		return """<html>
          	<head>
		  <link href="/static/css/style.css" rel="stylesheet">
		</head>
          	 <body>
		  <h1>Current setpoint is : </h1>
            	  <form method="get" action="staticsetpoint">
              	   <button type="submit">Static Temperature Set Point</button>
            	  </form>
		  <form method="get" action="dynamicsetpoint">
                   <button type="submit">Dynamic Temperature Profile</button>
          	 </body>
        	</html>"""

	@cherrypy.expose
	def staticsetpoint(self):
		return """<html>
                <head>
                  <link href="/static/css/style.css" rel="stylesheet">
                </head>
                 <body>
                  <form method="get" action="settemp">
		   <input type="text" value="66" name="setpoint" />
                   <button type="submit">Set Temperature (F)</button>
                  </form>
                 </body>
                </html>"""

	@cherrypy.expose
	def settemp(self, setpoint=0):
		return """<html>
                <head>
                  <link href="/static/css/style.css" rel="stylesheet">
                </head>
                 <body>
		  <h1>Temperature setpoint is now set to: %s</h1>
                  <form method="get" action="index">
                   <button type="submit">Home</button>
                  </form>
                 </body>
                </html>""" % setpoint		
	@cherrypy.expose
	def dynamicsetpoint(self):
		return """<html>
		<head>
		  <link href="/static/css/style.css" rel="stylesheet">
		</head>
		<body>
            	<h2>Upload a set point file</h2>
		<h3>This file should be formatted with one set-point pair per line. Format a pair as setpoint, days. For example: 67,2 <h3>
            	<form action="upload" method="post" enctype="multipart/form-data">
            	filename: <input type="file" name="myFile" /><br />
                <input type="submit" />
		</form>
		<form method="get" action="index">
            	<input type="submit" />
                <button type="submit">Home</button>
		</form>
		</body>
		</html>"""

	@cherrypy.expose
	def upload(self, myFile):
		upload_path = os.path.normpath(os.path.abspath(os.getcwd()) + '/uploads/')
		upload_file = os.path.join(upload_path, "uploaded_file.txt")
		size = 0
		with open(upload_file, 'wb') as out:
			while True:
				data = myFile.file.read(8192)
				if not data:
					break
				out.write(data)
				size += len(data)
		out = """<html>
		<body>
			myFile length: %s<br />
			myFile filename: %s<br />
			myFile mime-type: %s
		</body>
		</html>"""

		return out % (size, myFile.filename, myFile.content_type)




if __name__ == '__main__':
	conf = {
        	'/': {
            		#'tools.sessions.on': True,
            		'tools.staticdir.root': os.path.abspath(os.getcwd())
        	},
        	'/static': {
            		'tools.staticdir.on': True,
            		'tools.staticdir.dir': './public'
        	}
	}
	cherrypy.server.socket_host = '192.168.1.171' # put it here 
	cherrypy.quickstart(FermentationStation(), '/', conf)
