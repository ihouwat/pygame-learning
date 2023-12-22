
from typing import Tuple

import pygame
from config.settings import FONT_NAME, FONT_SMALL
from models.types import Color, Language


class StatusBar:
	""" A status bar that displays the score and level."""
	def __init__(self, rect: pygame.Rect):
		self.rect: pygame.Rect = rect
		font = pygame.font.match_font(FONT_NAME)
		self.font = pygame.font.Font(font, FONT_SMALL)
		self.text_color = pygame.Color(Color.WHITE.value)
		self.background_color = pygame.Color('black')
	
	def update(self, player_name: str, score: int, level: int, language: Language) -> list[Tuple[pygame.Surface, Tuple[int, int]]]:
		""" Updates the score and level and returns the content of the status bar."""
		player_name_surface = self.font.render(f'Good luck {player_name}!', True, self.text_color, self.background_color)
		language_surface = self.font.render(f'Language: {language.value}', True, self.text_color, self.background_color)
		level_surface = self.font.render(f'Level: {level}', True, self.text_color, self.background_color)
		score_surface = self.font.render(f'Score: {score}', True, self.text_color, self.background_color)
		
		line_height = self.font.get_linesize()
		return [(surface, (0, line_height * i+1)) for i, surface in enumerate([player_name_surface, language_surface, level_surface, score_surface]) ]