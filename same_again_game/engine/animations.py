from typing import Protocol

import pygame
from config.settings import FONT_NAME, FONT_REGULAR, SCREEN_HEIGHT, SCREEN_WIDTH
from engine.renderer import Renderer
from game_objects.item_sprite import ItemSprite
from models.game_types import Color
from pygame.sprite import Group
from ui.status_bar import StatusBar
from ui.ui_display import UIDisplay


class Animation(Protocol):
	
	def update(self) -> None:
		...
	
	@property
	def is_finished(self) -> bool:
		...

class ScaleSprites(Animation):
	
	def __init__(self, scaling_factor: float, renderer: Renderer, items: Group, item_to_match: ItemSprite, status_bar: StatusBar, ui_display: UIDisplay, draw_transitions: bool = False):
		self.scaling_factor = scaling_factor
		self.renderer = renderer
		self.items = items
		self.item_to_match = item_to_match
		self.draw_transitions = draw_transitions
		self.status_bar = status_bar
		self.ui_display = ui_display
		self._is_finished = False
	
	def update(self) -> None:
		self.scale_sprites(self.scaling_factor, self.items, self.item_to_match, self.draw_transitions)
		self.is_finished = True
	
	@property
	def is_finished(self) -> bool:
		return self._is_finished

	@is_finished.setter
	def is_finished(self, value: bool) -> None:
		self._is_finished = value
	
	def scale_sprites(self, scaling_factor: float, items: Group, item_to_match: ItemSprite, draw_transitions: bool = False) -> None:
		""" Scales sprites up or down.

		Args:
			scaling_factor (float): The amount to scale the sprite by.
			items (Group): The group of sprites to scale.
			item_to_match (ItemSprite): The item to match.
			draw_transitions (bool): Whether or not to draw the transitions. Defaults to False.
		"""
		sprites: list[ItemSprite] = [item_to_match] + items.sprites()

		def execute_animation():
			self.animate_sprite_scale(scaling_factor=scaling_factor, sprite=sprite, item_to_match=item_to_match, items=items, draw_transitions=draw_transitions)

		for sprite in sprites:
			if scaling_factor < 0:
				while sprite.scale > 0:
					execute_animation()
				pygame.time.wait(10)
			else:
				while sprite.scale < 100:
					execute_animation()
				pygame.time.wait(10)
	
	def animate_sprite_scale(self, scaling_factor: float, sprite: ItemSprite, items: Group, item_to_match: ItemSprite, draw_transitions: bool = False) -> None:
		sprite.scale_by(scaling_factor=scaling_factor)
		if draw_transitions:
			self.renderer.draw(item_to_match=item_to_match, items=items, status_bar=self.status_bar, ui_display=self.ui_display)
		pygame.display.update()

class LevelTransition(Animation):
	
	def __init__(self, renderer: Renderer, status_bar: StatusBar, ui_display: UIDisplay, level_number: int):
		self.renderer = renderer
		self.status_bar = status_bar
		self.ui_display = ui_display
		self.level_number = level_number
		self._is_finished = False
	
	def update(self) -> None:
		self.animate_level_transition(self.level_number)
		self.is_finished = True
	
	@property
	def is_finished(self) -> bool:
		return self._is_finished

	@is_finished.setter
	def is_finished(self, value: bool) -> None:
		self._is_finished = value
	
	def animate_level_transition(self, level_number: int) -> None:
		font = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_REGULAR)
		text_color = pygame.Color(Color.WHITE.value)
		text = font.render(f'Level {level_number}', True, text_color)
		y = (SCREEN_HEIGHT // 2) - FONT_REGULAR
		x = 0 - FONT_REGULAR

		pygame.time.wait(250)
		while x < SCREEN_WIDTH + 100:
			self.renderer.render_level_transition_animation(text, (x, y), self.status_bar, self.ui_display)
			x += 1
			pygame.display.flip()

class SpriteHoverEffect(Animation):
	
	def __init__(self, renderer: Renderer, status_bar: StatusBar, ui_display: UIDisplay, items: Group, min_scale: float, max_scale: float):
		self.renderer = renderer
		self.ui_display = ui_display
		self.items = items
		self.min_scale = min_scale
		self.max_scale = max_scale
		self._is_finished = False

	def update(self) -> None:
		self.animate_sprites_on_hover(self.items, self.min_scale, self.max_scale)
		self.is_finished = True
	
	@property
	def is_finished(self) -> bool:
		return self._is_finished

	@is_finished.setter
	def is_finished(self, value: bool) -> None:
		self._is_finished = value
	
	def animate_sprites_on_hover(self, items: Group, min_scale: float, max_scale: float) -> None:
		item_sprites: list[ItemSprite] = items.sprites()
		for sprite in item_sprites:
			if sprite.rect.collidepoint(pygame.mouse.get_pos()):
				if sprite.scale < max_scale:
					sprite.scale_by(scaling_factor=6)
			else:
				if sprite.scale > min_scale:
					sprite.scale_by(scaling_factor=-7)
