from typing import List, Tuple

import pygame
import pygame_menu
from config.settings import SCREEN_HEIGHT, SCREEN_WIDTH, START_GAME
from models.game_types import Language
from pygame_menu import events, themes


class GameMenu:
	def __init__(self):
		""" Creates a game menu."""
		self.languages: list[Tuple[str, int]] = list(tuple([(language.name, index) for index, language in enumerate(Language)]))
		self.selected_language = self.languages[0]
		self.player_name: str = ""
		self.menu: pygame_menu.Menu = pygame_menu.Menu('Same Again!', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=themes.THEME_BLUE)
		self.menu.add.text_input('Name: ', default='', onchange=self.set_name)
		self.menu.add.selector(title='Language :', items=self.languages, onchange=self.set_language)
		self.menu.add.button('Play', self.start_the_game)
		self.menu.add.button('Quit', events.EXIT)

	def start_the_game(self) -> None:
		""" Starts the game."""
		self.menu.disable()
		pygame.event.post(pygame.event.Event(START_GAME, {'language': self.selected_language[0], 'player': self.player_name}))
	
	def set_language(self, value: list[Tuple[str, int]], index: int) -> None:
		""" Sets the language for the game."""
		print('Language set to {}'.format(value))
		self.selected_language = self.languages[index]
	
	def set_name(self, value: str) -> None:
		""" Sets the player's name."""
		print('Name set to {}'.format(value))
		self.player_name = value

	def run(self, surface) -> None:
		""" Runs the menu."""
		# Use the surface created in __init__
		self.menu.mainloop(surface)