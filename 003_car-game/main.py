from game_objects.Player import Player
from game_objects.Enemy import Enemy
import pygame as pg, sys
from pygame.locals import *
from config.settings import WHITE, SCREEN_HEIGHT, SCREEN_WIDTH, FPS

# initialize game
pg.init()

FramesPerSec = pg.time.Clock()

# configure game window
DISPLAYSURF = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pg.display.set_caption("Car Game")

# create characters
Player1 = Player()
Enemy1 = Enemy()

while True:
	for event in pg.event.get():
		if event.type == QUIT:
			pg.quit()
			sys.exit()
	
	# update character state
	Player1.update()
	Enemy1.move()

	# refresh the screen
	DISPLAYSURF.fill(WHITE)
	#  draw the characters on the screen
	Player1.draw(DISPLAYSURF)
	Enemy1.draw(DISPLAYSURF)

	#  update the screen
	pg.display.update()
	# Ensure the game loop is running at 60 frames per second
	FramesPerSec.tick(FPS)