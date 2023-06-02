# TODO: both this script and the modules within will almost definitely need to be entirely refactored to get rid of the generic-ass names.

from re import L
from remote_module import remote_module
import pygame
import os


def id_all():
	print("ID command received! Calling all module's ID function.")
	rmod_audio.id()

class rmod_audio(remote_module):

	def __init__(self, cfg):		
		# Configure pygame
		SOUNDLIB_PATH = os.getcwd() + "\\sound_library\\" 
		print(SOUNDLIB_PATH)
		D_SAMPLERATE = cfg['Audio'].getint('SampleRate')
		D_AUDIOBUFFER =  cfg['Audio'].getint('Buffer')
		pygame.mixer.init(D_SAMPLERATE, -16, 2, D_AUDIOBUFFER)
		
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
		self.sound_library["rs"].play()

	def play(self, args):
		sound = self.sound_library[args[0]]
		if sound is not None:
			# Slightly bodgy method to ensure a sound always plays, even if it chokes all other concurrent sounds.
			if pygame.mixer.find_channel() is None:
				pygame.mixer.stop()
			sound.play() #pygame.mixer.Sound.play(sound)
		else:
			print("Could not find sound %s in sound library" % args[0])
	
	def play(self):
		self.play( [self.test_sound] )



	def parse_command(self, args):
		if args[0] == "play":
			self.play(args[1:])
	
	def id(self):
		self.play()

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

