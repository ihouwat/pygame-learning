from typing import Protocol

import pygame
from game_objects.item_sprite import ItemSprite
from game_objects.text_element import TextElement
from pygame.sprite import Group


class Animation(Protocol):
	""" Animation is the base class for all animations. """
	def update(self) -> None:
		""" Where the animation logic is executed. """
		...
	
	@property
	def is_finished(self) -> bool:
		""" Whether or not the animation is finished. """
		...

class ScaleSprite(Animation):
	""" ScaleSprite is responsible for scaling sprites up or down."""
	def __init__(self, scaling_factor: float, sprite: ItemSprite):
		self.scaling_factor = scaling_factor
		self.sprite = sprite
		self._is_finished = False
	
	def update(self) -> None:
		self.scale_sprites(self.scaling_factor, self.sprite)
		self.is_finished = True
	
	@property
	def is_finished(self) -> bool:
		return self._is_finished

	@is_finished.setter
	def is_finished(self, value: bool) -> None:
		self._is_finished = value
	
	def scale_sprites(self, scaling_factor: float, sprite: ItemSprite) -> None:
		""" Scales sprites up or down.

		Args:
			scaling_factor (float): The amount to scale the sprite by.
			items (Group): The group of sprites to scale.
			item_to_match (ItemSprite): The item to match.
			draw_transitions (bool): Whether or not to draw the transitions. Defaults to False.
		"""

		def execute_animation():
			self.animate_sprite_scale(scaling_factor=scaling_factor, sprite=sprite)

		if scaling_factor < 0:
			if sprite.scale >= 0:
				execute_animation()
		else:
			if sprite.scale <= 100:
				execute_animation()
	
	def animate_sprite_scale(self, scaling_factor: float, sprite: ItemSprite) -> None:
		sprite.scale_by(scaling_factor=scaling_factor)

class TextTransition(Animation):
	""" TextTransition is responsible for animating the text transition between levels."""
	
	def __init__(self, text_element: TextElement, x_increment: int = 1, y_increment: int = 0):
		self.text_element = text_element
		self.x_increment = x_increment
		self.y_increment = y_increment
		self._is_finished = False
	
	def update(self) -> None:
		self.text_element.set_position(self.text_element.current_position[0] + self.x_increment, self.text_element.current_position[1] + self.y_increment)
		self.is_finished = True
	
	@property
	def is_finished(self) -> bool:
		return self._is_finished

	@is_finished.setter
	def is_finished(self, value: bool) -> None:
		self._is_finished = value

class SpriteHoverEffect(Animation):
	""" SpriteHoverEffect is responsible for animating the hover effect on sprites."""
	def __init__(self, items: Group, min_scale: float, max_scale: float):
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
					sprite.scale_by(scaling_factor=10)
			else:
				if sprite.scale > min_scale:
					sprite.scale_by(scaling_factor=-7)
