# light_server.py

import socket
import RPi.GPIO as gpio
import datetime
import sys
import traceback

power = False
pin_number = 2
addr = ("10.100.102.44", 4444)
debug_mode = True

def toggle():
	power = not power
	if debug_mode:
		gpio.output(pin_number, power);
	else:
		print "toggle() called, changed power to %s" % (str(power))


def setup():
	if not debug_mode:
		gpio.setmode(gpio.BCM)
		gpio.setup(pin_number, gpio.OUT)
	else:
		print "setup() called"

def log(msg):
	f = open("log.txt", "a+")
    d = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    f.write(str(d) + ":")
    f.write(msg)
    f.write("\n\n")
    f.close()


def handle_request(client_socket):
	try:
		# print "toggled %s " % str(power)

		msg = client_socket.recv(1024)
		print "got:", msg

		toggle()  # Perform a toggle to the light
		client_socket.send(("Power: " + str(power)).encode())
		client.close()
	except:
		log("ERROR OCCURED")
		log(str(sys.exc_info()))
		log(traceback.format_exc())
		client.close()

if __name__ == "main":
	# Initial setup
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(addr)
	server.listen(5)
	setup()

	while 1:
		print "Waiting on incoming connections..."
		(client, c_addr) = server.accept()
		handle_request(client) # TODO: Do that on a different thread

