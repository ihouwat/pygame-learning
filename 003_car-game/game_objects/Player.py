import pygame as pg
from pygame.locals import *
from config.settings import SCREEN_WIDTH
import os
import pathlib

class Player (pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		# load the image
		self.image = pg.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).parent.absolute()), 'assets', 'images', 'player.png'))
		# automatically create a rectangle from the image
		self.rect = self.image.get_rect()
		# define a starting position for the rectangle (this helps us align the Rect with the image)
		self.rect.center = (160, 520)
	
	def update(self):
		pressed_keys = pg.key.get_pressed()
	# this game does not require up or down movements, but this is included for completeness
	# if pressed_keys[K_UP]:
	# 	self.rect.move_ip(0, -5)
	# if pressed_keys[K_DOWN]:
	# 	self.rect.move_ip(0, 5)

		# ensure the player does not move off-screen
		if self.rect.left > 0:
			if pressed_keys[K_LEFT]:
				self.rect.move_ip(-5, 0)
		if self.rect.right < SCREEN_WIDTH:
			if pressed_keys[K_RIGHT]:
				self.rect.move_ip(5, 0)

	def draw(self, surface):
		# blit takes two inputs, first the surface to be drawn, and then the object with which we want to draw
		surface.blit(self.image, self.rect)