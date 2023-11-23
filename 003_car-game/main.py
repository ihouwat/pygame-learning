from game_objects.Player import Player
from game_objects.Enemy import Enemy
import pygame as pg, sys
from pygame.locals import *
from config.settings import WHITE, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, INC_SPEED, SPEED, RED
import time

# initialize game
pg.init()

FramesPerSec = pg.time.Clock()

# configure game window with white screen and title
DISPLAYSURF = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pg.display.set_caption("Car Game")

# create Sprites
Player1 = Player()
Enemy1 = Enemy()

# create Sprite Groups
enemies = pg.sprite.Group()
enemies.add(Enemy1)
all_sprites = pg.sprite.Group()
all_sprites.add(Player1)
all_sprites.add(Enemy1)

# trigger user event
pg.time.set_timer(INC_SPEED, 5000)

# Game loop
while True:
	
	# Cycle through events
	for event in pg.event.get():
		# increase enemy speed if the INC_SPEED user event is triggered
		if event.type == INC_SPEED:
			SPEED += 1
		if event.type == QUIT:
			pg.quit()
			sys.exit()
	
	# update character state
	Player1.update()
	Enemy1.move()

	# refresh the screen
	DISPLAYSURF.fill(WHITE)

	# move and redraw all sprites
	for entity in all_sprites:
		DISPLAYSURF.blit(entity.image, entity.rect)
		entity.move(SPEED) # not the cleanest interface since Player doesn't need this, but it works for now
	
	# To check for collisions between Player and Enemy
	if pg.sprite.spritecollideany(Player1, enemies):
		# if the player touches any of the sprites in the enemies group
		# turn the screen red
		DISPLAYSURF.fill(RED)
		pg.display.update()
		for entity in all_sprites:
			# remove all sprites from the group to prevent re-drawing
			entity.kill()
		time.sleep(2)
		pg.quit()
		sys.exit()

	#  update the screen
	pg.display.update()
	# Ensure the game loop is running at 60 frames per second
	FramesPerSec.tick(FPS)