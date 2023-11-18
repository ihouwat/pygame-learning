from cevent import CEvent
import pygame
from pygame.locals import *

# inherit from CEvent class
class App(CEvent):
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
	
	def on_loop(self):
		pass
	
	def on_render(self):
		pass

	def on_cleanup(self):
		#  quits all PyGame modules and anything else is cleaned up by Python
		pygame.quit()
	
	# Override method from parent CEvent class
	# Flow: on_event -> event.type == QUIT -> on_exit (in App class) -> self._running = False -> on_cleanup
	def on_exit(self):
		self._running = False

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

if __name__ == "__main__":
	theApp = App()
	theApp.on_execute()