import RPi.GPIO as GPIO
import time
import os 
from http.server import BaseHTTPRequestHandler, HTTPServer
host_name = "192.168.140.207"
host_port = 8000
LED = 0
class MyServer(BaseHTTPRequestHandler):
	global LED
	def do_HEAD(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	def do_GET(self):
		global LED
		html = '''
			<html>
			<body style="width:960px;margin: 20px auto;">
			<h1>LED Control</h1>
			<p>Turn LED on: <a href = "/on">Start/Stop </a></p>
			</body>
			</html>
		'''
		temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
		self.do_HEAD()
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(4, GPIO.OUT)
		status = ''
		if self.path=='/on':
			GPIO.output(4, GPIO.LOW)
			time.sleep(0.5)
			GPIO.output(4, GPIO.HIGH)
			status= 'LED is off'
		print(LED)
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(4, GPIO.OUT)
		
		self.wfile.write(html.format(temp[5:], status).encode("utf-8"))
if __name__=='__main__':
	http_server = HTTPServer((host_name, host_port), MyServer)
	print("Server Starts - %s:%s"%(host_name, host_port))
	try:
		http_server.serve_forever()
	except KeyboardInterrupt:
		http_server.server_close()

