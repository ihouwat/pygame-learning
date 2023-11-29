import pygame
from pygame.locals import *
import sys
import random
from tkinter import * # Tkinter is a GUI library that comes with Python
from tkinter import filedialog

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
	def __init_(self):
		super().__init__()
		
class Ground(pygame.sprite.Sprite):
	def __init_(self):
		super().__init__()

class Player(pygame.sprite.Sprite):
	def __init_(self):
		super().__init__()

class Enemy(pygame.sprite.Sprite):
	def __init_(self):
		super().__init__()


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

		
	