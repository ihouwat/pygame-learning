import os
import pathlib
import random

import config.settings as config
import pygame as pg
from config.settings import SCREEN_HEIGHT, SCREEN_WIDTH, SPEED


class Enemy (pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pg.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).parent.absolute()), 'assets', 'images', 'enemy.png'))
		self.rect = self.image.get_rect()
		# randomize the starting position on the X axis
		self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
	
	def move(self, speed = SPEED):
		# move down the Y axis, speed is variable
		self.rect.move_ip(0, speed)
		if (self.rect.bottom > SCREEN_HEIGHT):
			self.update_score()
			self.rect.top = 0
			# randomize the starting position on the X axis
			self.rect.center = (random.randint(30, 370), 0)
	
	def update_score(self):
		config.SCORE = config.SCORE + 1

# Blitting not needed for the individual object, as we are drawing in the main loop
""" 
	def draw(self, surface):
		surface.blit(self.image, self.rect) 
"""