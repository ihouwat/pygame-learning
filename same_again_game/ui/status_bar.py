
from typing import Tuple

import pygame
from config.settings import FONT_NAME, FONT_SMALL
from game_objects.text_element import TextElement
from models.game_types import Color
from ui.ui_display import UIDisplay


class StatusBar:
	""" A status bar that displays the score and level.
	
	Attributes:
		x_coordinate(int): The x coordinate of the status bar.
		y_coordinate(int): The y coordinate of the status bar.
		font(pygame.font.Font): The font to be used for the text elements.
		text_color(pygame.Color): The color of the text elements.
		background_color(pygame.Color): The background color of the status bar.
		player_name(TextElement): The text element for the player name.
		language(TextElement): The text element for the language.
		level(TextElement): The text element for the level.
		score(TextElement): The text element for the score.
	"""
	def __init__(self, x_coordinate: int = 0, y_coordinate: int = 0):
		self.x_coordinate = x_coordinate
		self.y_coordinate = y_coordinate
		self.font = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_SMALL)
		self.text_color = pygame.Color(Color.WHITE.value)
		self.background_color = pygame.Color('black')

		# Initialize the text elements
		self.player_name = TextElement('', self.font, self.text_color, 0, 0)
		self.language = TextElement('', self.font, self.text_color, 0, 0)
		self.level = TextElement('', self.font, self.text_color, 0, 0)
		self.score = TextElement('', self.font, self.text_color, 0, 0)
	
	def update(self, ui_display: UIDisplay) -> list[Tuple[pygame.Surface, Tuple[int, int]]]:
		""" Updates the status bar text content and returns the surfaces to be render.

		Args:
			ui_display(UIDisplay): The UI display object.
			
		Returns:
			list[Tuple[pygame.Surface, Tuple[int, int]]]: The surfaces to be rendered and their coordinates
		"""
		self.player_name.set_text(f'Good luck {ui_display.player_name}!')
		self.language.set_text(f'Language: {ui_display.language.value}')
		self.level.set_text(f'Level: {ui_display.level}')
		self.score.set_text(f'Score: {ui_display.score}')
		
		line_height = self.font.get_linesize()
		return [(surface.draw(), (self.x_coordinate, self.y_coordinate + (line_height * i+1))) for i, surface in enumerate([self.player_name, self.language, self.level, self.score]) ]