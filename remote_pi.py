import socket
import netifaces
import pygame
import time
import configparser

import modules
import remote_base

def ping(): 
	pass

BASE_COMMANDS = {
	'poke' : ping,
	'id' : modules.id_all
}

cfg = configparser.ConfigParser()
cfg.read('default.ini')

# Get custom configuration and overrite default vals
custom_cfg = configparser.ConfigParser()
custom_cfg.read('config.ini')
for sect in custom_cfg.sections():
	for (key, val) in custom_cfg.items(sect):
		cfg[sect][key] = val

def print_cfg(cfg):
	for sect in cfg.sections():
		print(str(sect))
		for (key, val) in cfg.items(sect):
			print("- " + str(key) + ": " + str(val))
print_cfg(cfg)


audio = modules.rmod_audio(cfg)
arduino = modules.rmod_arduino(cfg)

# Configure server
PORT = cfg['General'].getint('Port')
IP = ""
while IP == "":
	try:
		IP = netifaces.ifaddresses(cfg['General']['Interface'])[netifaces.AF_INET][0]['addr']
	except KeyError:
		print("IP Address retrieval failed. Check this device's internet connection (Using adapter " + cfg['General']['Interface'] + "). Retrying in 5 seconds.")
		time.sleep(5)

print("\nStarting RemotePi Server with IP " + str(IP) + " and port " + str(PORT))

pi_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pi_socket.bind((IP, PORT))
print("Socket running")

pi_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)

# Server loop
while True:
	data, addr = pi_socket.recvfrom(1024)
	data = data.decode()
	
	# TODO: allow skipping any base messages like poke or ID
	print("Received: " + str(data))
	
	if data[0] == "/":
		data = data[1:] # remove opening /
		args = data.split("/") # collect each phrase of command
		func = args.pop(0) # place command name in func to make structure similar to Unity

		if func in BASE_COMMANDS:
			if func == 'id':
				audio.id()
			BASE_COMMANDS[func]()
		else: 
			# Case for standard commands
			print("Function /" + func + "/ called with arguments " + str(args))
			
			if func == "audio":
				audio.parse_command(args)
			if func == "arduino":
				arduino.parse_command(args)
	else:
		print("Discarding, does not include initial \'/\'")
	print() 
