import pygame
from pygame.locals import *
import sys
import random
from tkinter import * # Tkinter is a GUI library that comes with Python
from tkinter import filedialog
import os
import pathlib

pygame.init() # Begin pygame

# Declare variables
vec = pygame.math.Vector2 # has two components (x,y), which we'll use to track the Player sprite
HEIGHT = 350 # screen height
WIDTH = 700 # screen width
ACC = 0.3 # Acceleration
FRIC = -0.10 # Friction
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG") # Window title

# Classes
class Background(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.bgimage = pygame.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), 'Background.png'))
		self.bgY = 0
		self.bgX = 0
	
	def render(self):
		displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
		
class Ground(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), 'Ground.png'))
		self.rect = self.image.get_rect(center = (350, 350)) # rect is a must in order to interact with other objects
	
	def render(self):
		displaysurface.blit(self.image, (self.rect.x, self.rect.y))

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), 'Player_Sprite_R.png'))
		self.rect = self.image.get_rect()
	
		# Position and direction
		self.vx = 0
		self.pos = vec((340, 240)) # position
		self.vel = vec(0,0) # velocity
		self.acc = vec(0,0) # acceleration
		self.direction = "RIGHT" # direction
	
	def move(self):
		pass
	
	def update(self):
		pass

	def attack(self):
		pass

	def jump(self):
		pass

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

# Instantiate classes
background = Background()
ground = Ground()
player = Player()

# Game loop
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		# left click
		if event.type == MOUSEBUTTONDOWN: 
			pass

		if event.type == KEYDOWN:
			pass
	
	# Rendering
	background.render()
	ground.render()
	displaysurface.blit(player.image, player.rect)

	pygame.display.update()
	FPS_CLOCK.tick(FPS)
