
from typing import Tuple

import pygame
from config.settings import FONT_NAME, FONT_SMALL
from models.game_types import Color
from ui.ui_display import UIDisplay


class StatusBar:
	""" A status bar that displays the score and level."""
	def __init__(self, x_coordinate: int = 0, y_coordinate: int = 0):
		self.x_coordinate = x_coordinate
		self.y_coordinate = y_coordinate	
		self.font = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_SMALL)
		self.text_color = pygame.Color(Color.WHITE.value)
		self.background_color = pygame.Color('black')
	
	def update(self, ui_display: UIDisplay) -> list[Tuple[pygame.Surface, Tuple[int, int]]]:
		""" Updates the score and level and returns the content of the status bar."""
		player_name_surface = self.font.render(f'Good luck {ui_display.player_name}!', True, self.text_color, self.background_color)
		language_surface = self.font.render(f'Language: {ui_display.language.value}', True, self.text_color, self.background_color)
		level_surface = self.font.render(f'Level: {ui_display.level}', True, self.text_color, self.background_color)
		score_surface = self.font.render(f'Score: {ui_display.score}', True, self.text_color, self.background_color)
		
		line_height = self.font.get_linesize()
		return [(surface, (self.x_coordinate, self.y_coordinate + (line_height * i+1))) for i, surface in enumerate([player_name_surface, language_surface, level_surface, score_surface]) ]