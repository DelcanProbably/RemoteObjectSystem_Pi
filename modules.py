# NOTE: The modules system will likely dramatically change in future versions of ROS

from re import L
from remote_module import remote_module
import pygame
import os
import pyduino


def id_all():
	print("ID command received! Calling all module's ID function.")
	# rmod_audio.id()
	# wait durrr i can't call that statically... will need to come up with another way of doing that

class rmod_audio(remote_module):

	def __init__(self, cfg):		
		# Configure pygame
		SOUNDLIB_PATH = os.getcwd() + "/sound_library/" 
		print(SOUNDLIB_PATH)
		D_SAMPLERATE = cfg['Audio'].getint('SampleRate')
		D_AUDIOBUFFER =  cfg['Audio'].getint('Buffer')
		pygame.mixer.init(D_SAMPLERATE, -16, 2, D_AUDIOBUFFER)
		
		self.play_volume = 1
		
		# Create sound library populated with all sounds in the sound library folder.
		self.sound_library = {}
		self.test_sound = ""
		for f in os.listdir(SOUNDLIB_PATH):
			sound_name = f.split(".")[0]
			self.sound_library[sound_name] = pygame.mixer.Sound(SOUNDLIB_PATH + f)
			
			# TODO: There should be a way to explicitly specify a test sound, or to look for a particular filename for the test sound.
			if self.test_sound == "":
				self.test_sound = sound_name

		# test initialisation sound
		self.sound_library["test"].play()

	def play(self, args):
		sound = self.sound_library[args[0]]
		vol = self.play_volume
		if len(args) > 1:
			vol = args[1]
		sound.set_volume(float(vol))
		if sound is not None:
			# Slightly bodgy method to ensure a sound always plays, even if it chokes all other concurrent sounds.
			if pygame.mixer.find_channel() is None:
				pygame.mixer.stop()
			sound.play() #pygame.mixer.Sound.play(sound)
		else:
			print("Could not find sound %s in sound library" % args[0])

	def volume(self, args):
		self.play_volume = args[0]
		print("Set play volume to " + str(args[0]))

	def parse_command(self, args):
		# FIXME: surely python has some scuffed way to convert a string into a function name?
		if args[0] == "play":
			self.play(args[1:])
		elif args[0] == "volume":
			self.volume(args[1:])
	
	def id(self):
		self.sound_library["test"].play()


class rmod_arduino(remote_module):
	def __init__(self, cfg):
		try:
			self.a = pyduino.Arduino()
			self.pinmode([])
		except:
			self.a = None
			print("Could not find a connected Arduino, ignoring all /arduino/ commands")
		
	
	def dwrite(self, args):
		if len(args) != 2:
			print("Invalid number of arguments")
			return
		pin = int(args[0])
		val = int(args[1])
		self.a.digital_write(pin, val)
	
	def awrite(self, args):
		print("Not yet implemented")
		pass
	
	def pinmode(self, args):
		if len(args) == 0:
			print('Setting all pins to output')
			for i in range(13):
				self.a.set_pin_mode(i, 'O')
		elif len(args) >= 1:
			pin = int(args[0])
			mode = 'O'
			if len(args) > 1:
				mode = str(args[1])
			self.a.set_pin_mode(pin, mode)
			
	
	def parse_command(self, args):
		if self.a == None:
			print("No Arduino found in setup, ignoring.")
			return
		funcs = {
			'dwrite' : self.dwrite,
			'awrite' : self.awrite,
			'pinmode': self.pinmode
		}
		
		if args[0] in funcs:
			funcs[args[0]](args[1:])
	
	def id(self):
		pass

'''

Unfinished

class rmod_gpio(remote_module):
	def __init__(self, cfg):
		pass
	
	def setpin(self, args):
		pass

class rmod_input(remote_module):
	def __init__(self, cfg):
		self.target_ip = "127.0.0.1"
	
	def set_ip(self, ip):
		self.target_ip = ip
			
	def parse_command(self, args):
		if args[0] == "init":
			self.set_ip(args[1]) # TODO: init function instead of manually setting shit


class rmod_display(remote_module):
	def __init__(self, cfg):
		pass
	
	def parse_command(self, args):
		pass

class rmod_midi(remote_module):
	def __init__(self, cfg):
		pass
	
	def parse_command(self, args):
		pass
'''
