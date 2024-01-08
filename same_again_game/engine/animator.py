import pygame
from config.settings import ANIMATION_DELAY
from engine.animation_engine import AnimationEngine
from engine.animations import ScaleSprite, SpriteHoverEffect, TextTransition
from game_objects.item_sprite import ItemSprite
from game_objects.text_element import TextElement


class Animator:
	def __init__(self, animation_engine: AnimationEngine):
		self.animation_engine = animation_engine
	
	def transition_out_sprites(self, all_sprites: list[ItemSprite], scale_factor: float) -> bool:
		""" Scales all sprites in the list to 0.0, and returns True if all sprites are scaled to 0.0.
	
		Parameters:
		all_sprites (list[ItemSprite]): The list of sprites to scale.
		scale_factor (float): The factor to scale the sprites by.

		Returns:
		bool: True if all sprites are scaled to 0.0, False otherwise.

		Raises:
		ValueError: If scale_factor is positive.
	"""
		if scale_factor > 0:
			raise ValueError("scale_factor must be negative.")

		if any(sprite.scale > 0 for sprite in all_sprites):
			self.scale_sprites(all_sprites, scale_factor)
			return False

		pygame.time.delay(ANIMATION_DELAY)
		return True

	def transition_in_sprites(self, all_sprites: list[ItemSprite], scale_factor: float) -> bool:
		""" Scales all sprites in the list to 1.0, and returns True if all sprites are scaled to 1.0.
	
		Parameters:
		all_sprites (list[ItemSprite]): The list of sprites to scale.
		scale_factor (float): The factor to scale the sprites by.

		Returns:
		bool: True if all sprites are scaled to 1.0, False otherwise.
	
		Raises:
		ValueError: If scale_factor is negative.
	"""
		if scale_factor < 0:
			raise ValueError("scale_factor must be positive.")

		if any(sprite.scale < 100 for sprite in all_sprites):
			self.scale_sprites(all_sprites, scale_factor)
			return False

		pygame.time.delay(ANIMATION_DELAY)
		return True

	def scale_sprites(self, sprites: list[ItemSprite], scale_factor: float) -> None:
		""" Scales all sprites in the list by the given scaling factor.

		Args:
		sprites (list[ItemSprite]): The list of sprites to scale.
		scale_factor (float): The factor to scale the sprites by.
		"""
		for sprite in sprites:
			self.animation_engine.add_animation(ScaleSprite(scaling_factor=scale_factor, sprite=sprite))
		self.animation_engine.execute()
	
	def animate_text_element_if_needed(self, text_element: TextElement, condition_to_animate: bool, x_increment: int, y_increment: int) -> bool:
		""" Animates the given text element if the given condition is True, and returns True if the animation is complete.
  
		Args:
		text_element (TextElement): The text element to animate.
		condition_to_animate (bool): The condition to animate the text element.
		x_increment (int): The x increment of the animation.
		y_increment (int): The y increment of the animation.

		Returns:
		bool: True if the animation is complete, False otherwise.
		"""
		if condition_to_animate:
			self.animate_text_element(text_element, x_increment, y_increment)
			return False
		return True

	def animate_text_element(self, text_element: TextElement, x_increment: int, y_increment: int) -> None:
		""" Animates the given text element by the given increments.
  
		Args:
		text_element (TextElement): The text element to animate.
		x_increment (int): The x increment of the animation.
		y_increment (int): The y increment of the animation.  
		"""
		self.animation_engine.add_animation(TextTransition(text_element=text_element, x_increment=x_increment, y_increment=y_increment)).execute()

	def hover_effect(self, items: pygame.sprite.Group, min_scale: int, max_scale: int) -> None:
		""" Adds a hover effect to the given items.

		Args:
		items (pygame.sprite.Group): The items to add the hover effect to.
		min_scale (int): The minimum scale of the hover effect, beyond which the hover effect will not scale.
		max_scale (int): The maximum scale of the hover effect, beyond which the hover effect will not scale.
		"""
		self.animation_engine.add_animation(SpriteHoverEffect(items=items, min_scale=min_scale, max_scale=max_scale)).execute()
