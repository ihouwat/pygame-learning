from typing import Tuple

import pygame
import pygame_menu
from config.settings import RESUME_GAME, SCREEN_HEIGHT, SCREEN_WIDTH, START_GAME
from models.game_types import Language
from pygame_menu import themes


class GameMenu:
	def __init__(self):
		""" Creates a game menu.

		Attributes:
			languages(list[Tuple[str, int]]): The languages available in the game.
			selected_language(Tuple[str, int]): The selected language.
			player_name(str): The name of the player.
			is_game_in_progress(bool): Indicates if a game is running.
			menu(pygame_menu.Menu): The menu.
		"""
		self.languages: list[Tuple[str, int]] = list(tuple([(language.name, index) for index, language in enumerate(Language)]))
		self.selected_language_index: int = 0
		self.player_name: str = ""
		self.is_game_in_progress: bool = False
		self.menu: pygame_menu.Menu = pygame_menu.Menu('Same Again!', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=themes.THEME_BLUE)
		
		self.configure_menu()

	def open_menu(self) -> None:
		""" Configures and enables the menu."""
		self.configure_menu()
		self.menu.enable()

	def configure_menu(self) -> None:
		""" Configures the menu depending on game state."""
		self.menu.clear()

		self.menu.add.text_input('Enter Your Name: ', default=self.player_name, onchange=self.set_name)
		self.menu.add.selector(title='Select Language :', default=self.selected_language_index, items=self.languages, onchange=self.set_language)
		
		if self.is_game_in_progress:
			self.menu.add.button('Save Settings', self.save_settings)
			self.menu.add.button('Start New Game', self.start_the_game)
			self.menu.add.button('Quit', self.quit_the_game)
		else:
			# player is about to start a new game
			self.menu.add.button('Start Game', self.start_the_game)
			self.menu.add.button('Quit', self.quit_the_game)

	def start_the_game(self) -> None:
		""" Starts the game and emits an event containing the player configured settings."""
		self.menu.disable()
		self.is_game_in_progress = True
		pygame.event.post(pygame.event.Event(START_GAME, {'language': self.languages[self.selected_language_index][0], 'player': self.player_name}))
	
	def resume_the_game(self) -> None:
		""" Starts the game."""
		self.menu.disable()
		self.is_game_in_progress = True
		pygame.event.post(pygame.event.Event(RESUME_GAME, {'language': self.selected_language[0], 'player': self.player_name}))
	
	def quit_the_game(self) -> None:
		""" Quits the game."""
		self.menu.disable()
		pygame.event.post(pygame.event.Event(pygame.QUIT))
	
	def set_language(self, value: list[Tuple[str, int]], index: int) -> None:
		""" Sets the language for the game."""
		print('Language set to {}'.format(value))
		self.selected_language = self.languages[index]
	
	def set_name(self, value: str) -> None:
		""" Sets the player's name."""
		print('Name set to {}'.format(value))
		self.player_name = value