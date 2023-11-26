import pygame as pg
import os, pathlib
from game_objects.Enemy import Enemy
from game_objects.Player import Player
from config.settings import FONT_NAME, FONT_REGULAR, BLACK, FONT_SMALL, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

def initialize_game():
	# create Sprites
	player1 = Player()
	enemy1 = Enemy()

	# create Sprite Groups
	enemies = pg.sprite.Group()
	enemies.add(enemy1)
	all_sprites = pg.sprite.Group()
	all_sprites.add(player1)
	all_sprites.add(enemy1)

	# define fonts
	font = pg.font.SysFont(FONT_NAME, FONT_REGULAR)
	font_small = pg.font.SysFont(FONT_NAME, FONT_SMALL)
	game_over_text = font.render("Game Over", True, BLACK)

	# Background image
	background = pg.image.load(os.path.join(os.path.dirname(pathlib.Path(__file__).parent.absolute()), 'assets', 'images', 'animated_street.png'))
	
	# configure game window with white screen
	display_surf = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	display_surf.fill(WHITE)

	# User events
	inc_speed_event = pg.USEREVENT + 1 # create user event and add one to ensure it has a unique ID

	dict = {
		'player1': player1,
		'enemies': enemies,
		'all_sprites': all_sprites,
		'font': font,
		'font_small': font_small,
		'game_over_text': game_over_text,
		'background': background,
		'display_surf': display_surf,
		'inc_speed_event': inc_speed_event
	}

	return dict
