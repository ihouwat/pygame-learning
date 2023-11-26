import pygame as pg 
import sys, os, pathlib
from pygame.locals import *
from config.settings import WHITE, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, SPEED, RED, BLACK
import config.settings as config
import config.setup as setup
import time
import pathlib

# initialize game
pg.init()
player1, enemies, all_sprites, font, font_small, game_over_text, background, display_surf, inc_speed_event = setup.initialize_game().values()

frames_per_sec = pg.time.Clock()
# set game window caption
pg.display.set_caption("Car Game")
# trigger user event object on a regular interval
pg.time.set_timer(inc_speed_event, 5000)

# Game Loop
while True:

	# Cycle through events
	for event in pg.event.get():
		# increase enemy speed if the inc_speed_event user event is triggered
		if event.type == inc_speed_event:
			SPEED += 0.5
		if event.type == QUIT:
			pg.quit()
			sys.exit()
	
	# Refresh the screen and display the score
	# Note it is important to draw the backround first, as Pygame has a layer system. 
	display_surf.blit(background, (0,0))
	scores = font_small.render(str(config.SCORE), True, BLACK)
	display_surf.blit(scores, (10,10))

	# move and redraw all sprites
	for entity in all_sprites:
		display_surf.blit(entity.image, entity.rect)
		entity.move(SPEED) # not the cleanest interface since Player doesn't need this, but it works for now
	
	# On collision between Player and any Enemy
	if pg.sprite.spritecollideany(player1, enemies):
		# Play a crash sound
		pg.mixer.Sound(os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), 'assets', 'audio', 'crash.wav')).play()
		time.sleep(0.5)

		# turn the screen red and display the game over text
		display_surf.fill(RED)
		display_surf.blit(game_over_text, (30, 250))
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
	frames_per_sec.tick(FPS)