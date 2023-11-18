import pygame
from pygame.locals import *

class App:
	def __init__(self) -> None:
		self._running = True
		self._display_surf = None
		self.size = self.weight, self.height = 640, 400

	# This function is called when the program starts. It can be used to initialize everything you need.
	def on_init(self) -> bool:
		# initialize the pygame modules
		pygame.init()
		# set screen size and try to use hardware acceleration
		self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True
	
	# Scans for events, and sets _running to False to break the game loop.
	def on_event(self, event) -> None:
		if event.type == pygame.QUIT:
			print('Quitting the game')
			self._running = False
	
	def on_loop(self):
		pass
	
	def on_render(self):
		pass

	def on_cleanup(self):
		#  quits all PyGame modules and anything else is cleaned up by Python
		pygame.quit()

	#  initializes pygame, enters the main loop which checks for events, computes and renders the game, until the game is over. Before exiting, it cleans up the pygame modules.
	def on_execute(self):
		if self.on_init() == False:
			self._running = False
			
		while( self._running ):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()

""" 
Before executing a program, the Python interpreter assigns the name of the python module into a special variable called __name__.
Depending on whether you are executing the program through command line or importing the module into another module, the assignment for __name__ will vary.
"""
if __name__ == "__main__":
	theApp = App()
	theApp.on_execute()