import pygame as pg
import random
from config.settings import SCREEN_HEIGHT
import os
import pathlib

class Enemy (pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pg.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).parent.absolute()), 'assets', 'images', 'enemy.png'))
		self.rect = self.image.get_rect()
		self.rect.center = (160, 520)
	
	def move(self):
		self.rect.move_ip(0, 10)
		if (self.rect.bottom > SCREEN_HEIGHT):
			self.rect.top = 0
			# randomize the starting position of the enemy
			self.rect.center = (random.randint(30, 370), 0)

	def draw(self, surface):
		surface.blit(self.image, self.rect)