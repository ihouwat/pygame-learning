import pygame as pg
from pygame.locals import *
from config.settings import SCREEN_WIDTH
import os
import pathlib

class Player (pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pg.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).parent.absolute()), 'assets', 'images', 'player.png'))
		self.rect = self.image.get_rect()
		self.rect.center = (160, 520)
	
	def update(self):
		pressed_keys = pg.key.get_pressed()
	# if pressed_keys[K_UP]:
	# 	self.rect.move_ip(0, -5)
	# if pressed_keys[K_DOWN]:
	# 	self.rect.move_ip(0, 5)

		if self.rect.left > 0:
			if pressed_keys[K_LEFT]:
				self.rect.move_ip(-5, 0)
		if self.rect.right < SCREEN_WIDTH:
			if pressed_keys[K_RIGHT]:
				self.rect.move_ip(0, 5)

	def draw(self, surface):
		surface.blit(self.image, self.rect)