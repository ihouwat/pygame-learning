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
		self.jumping = False # jumping
	
	def move(self):
		# Keep a constant acceleration of 0.5 in the downard direction (gravity)
		self.acc = vec(0, 0.5)

		# we can check if the players has slowed down to a certain extent 
		if abs(self.vel.x) > 0.3:
			self.running = True 
		else:
			self.running = False

		# returns the current key presses
		pressed_keys = pygame.key.get_pressed()
  
		# Accelerates sthe player in the direction of the key press
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = ACC

		# Formulas to calculate velocity while accounting for friction
		# Gist of it is that acceleration is calculated based off velocity and friction, and the position is updated based off how much distance was covered (based on acceleration and velocity)
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc # Updates the position with the new values

		# This causes character warping from one point of the screen to the other
		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

		# Update rect pos
		self.rect.midbottom = self.pos

	def update(self):
		pass

	def attack(self):
		pass

	def jump(self):
		# the self.rect.x += 1 and self.rect.x -= 1 is there to check for collisions on the x-axis
		self.rect.x += 1

		# Check to see if the player is on the ground
		hits = pygame.sprite.spritecollide(self, ground_group, False)

		self.rect.x -= 1
  
		# If touching the ground, and not currently jumping, cause the player to jump
		if hits and not self.jumping:
			self.jumping = True
			self.vel.y = -12 # negative y velocity means upwards

	def gravity_check(self):
		hits = pygame.sprite.spritecollide(player, ground_group, False)
		if self.vel.y > 0: # check if the player has downwards velocity, meaning they are falling
			if hits: # if there is a collision between the player and the ground
				lowest = hits[0]
				if self.pos.y < lowest.rect.bottom:
					self.pos.y = lowest.rect.top + 1
					self.vel.y = 0 # stop the player from falling
					self.jumping = False # allow the player to jump again

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

# Instantiate classes
background = Background()
ground = Ground()
player = Player()

# Sprite groups
ground_group = pygame.sprite.Group()
ground_group.add(ground)

# Game loop
while True:
	player.gravity_check() # first check if the player is on the ground

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		# left click
		if event.type == MOUSEBUTTONDOWN: 
			pass

		if event.type == KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.jump()
	
	# Rendering
	background.render()
	ground.render()
	player.move()
	displaysurface.blit(player.image, player.rect)

	pygame.display.update()
	FPS_CLOCK.tick(FPS)
