
from typing import Tuple

import pygame
from config.settings import FONT_NAME, FONT_SMALL
from config.types import Color


class StatusBar:
	""" A status bar that displays the score and level."""
	def __init__(self, rect: pygame.Rect):
		self.rect: pygame.Rect = rect
		font = pygame.font.match_font(FONT_NAME,)
		self.font = pygame.font.Font(font, FONT_SMALL)
		self.text_color = pygame.Color(Color.WHITE.value)
		self.background_color = pygame.Color('black')
	
	def update(self, score: int, level: int) -> list[Tuple[pygame.Surface, Tuple[int, int]]]:
		""" Updates the score and level and returns the content of the status bar."""
		level_surface = self.font.render(f'Level: {level}', True, self.text_color, self.background_color)
		score_surface = self.font.render(f'Score: {score}', True, self.text_color, self.background_color)
		return [(level_surface, (0, 0)), (score_surface, (0, level_surface.get_height()))]