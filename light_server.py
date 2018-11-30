# light_server.py

import socket
# import RPi.GPIO as gpio
import datetime
import sys
import traceback

power = None
pin_number = 2
# addr = ("10.100.102.44", 4444)
addr = ("127.0.0.1", 5555)
debug_mode = True

# Files
__light_state = "./light_state"
__log_filename = "./log/server_log"


# Responses
RESPONSE_TOGGLE = "TOGGLED"
RESPONSE_STATE_ON = "1"
RESPONSE_STATE_OFF = "0"
RESPONSE_BAD_REQUEST = "BAD_REQUEST"


def file_write(msg, filename):
	"""
	Logs a message to a desired file, fails if one
	of the arguments is not specified
	"""
	f = open(filename, "a+")
	d = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
	f.write(str(d) + ":")
	f.write(msg)
	f.write("\n\n")
	f.close()


def debug(msg):
	if debug_mode:
		file_write(msg, __log_filename)


def get_state():
	stat_file = open(__light_state, "r")
	ans = stat_file.read(1)  # Read 1 character, 0 or 1
	stat_file.close()
	# debug("read status: " + str(ans))
	return str(ans)

def set_state(stat):
	stat_file = open(__light_state, "w+")
	stat_file.write(stat)
	stat_file.close()
	# debug("wrote to file: " + str(stat))


def toggle():
	current_status = get_state()
	if current_status == "1":
		power = False  # if power was "1" (on) change it to false (off)
		set_state("0")
	elif current_status == "0":
		power = True
		set_state("1")
	else:
		log("ERROR! Read unexpected value from the state file at: " + __light_state + ": " + current_status)


	# remove this on live
	if not debug_mode:
		gpio.output(pin_number, power);
	else:
		print "toggle() called, changed power to %s" % (str(power))




def setup():
	if not debug_mode:
		gpio.setmode(gpio.BCM)
		gpio.setup(pin_number, gpio.OUT)
	else:
		print "setup() called"

	set_state("0")  # first, set it to OFF




def handle_request(client_socket):
	try:
		msg = client_socket.recv(1024)
		print "got:", msg

		ans = RESPONSE_BAD_REQUEST  # Default is bad request
		if msg.startswith("STATE"):
			ans = get_state()
			debug("status requested... answering with: " + ans)
		elif msg.startswith("TOGGLE"):
			toggle()  # Perform a toggle to the light
			ans = RESPONSE_TOGGLE
			debug("toggle requested... state changed to: " + ans)
		else:
			debug("Unexpected request: " + str(msg))

		client_socket.send(ans.encode())
		client_socket.close()
	except:
		log("FATAL ERROR OCCURED")
		log(str(sys.exc_info()))
		log(traceback.format_exc())
		client.close()

if __name__ == "__main__":
	# Initial setup
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(addr)
	server.listen(5)
	setup()

	while 1:
		print "Waiting on incoming connections on: ", addr
		(client, c_addr) = server.accept()
		print "Accepted connection"
		handle_request(client) # TODO: Do that on a different thread

