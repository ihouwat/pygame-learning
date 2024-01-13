import pygame
from config.settings import ANIMATION_DELAY
from engine.animation_engine import AnimationEngine
from engine.animations import ScaleSprite, SpriteHoverEffect, TextTransition
from game_objects.item_sprite import ItemSprite
from game_objects.text_element import TextElement


class Animator:
	def __init__(self, animation_engine: AnimationEngine):
		self.animation_engine = animation_engine
	
	def transition_out_sprites(self, all_sprites: list[ItemSprite], scale_factor: float, stagger_animation: bool = False) -> bool:
		""" Scales all sprites in the list to 0.0, and returns True if all sprites are scaled to 0.0.
	
		Parameters:
		all_sprites (list[ItemSprite]): The list of sprites to scale.
		scale_factor (float): The factor to scale the sprites by.
		stagger_animation (bool): Whether to stagger the animation by adding a delay.

		Returns:
		bool: True if all sprites are scaled to 0.0, False otherwise.

		Raises:
		ValueError: If scale_factor is positive.
	"""
		if scale_factor > 0:
			raise ValueError("scale_factor must be negative.")

		updated_sprites_list = all_sprites

		if stagger_animation:
			new_sprites = all_sprites[::-1]
			updated_sprites_list = [sprite for (i, sprite) in enumerate(new_sprites) if i == 0 or (i > 0 and new_sprites[i - 1].scale < 70)]
		
		if any(sprite.scale > 0 for sprite in updated_sprites_list):
			self.scale_sprites(updated_sprites_list, scale_factor)
			return False

		pygame.time.delay(ANIMATION_DELAY)
		return True

	def transition_in_sprites(self, all_sprites: list[ItemSprite], scale_factor: float, stagger_animation: bool = False) -> bool:
		""" Scales all sprites in the list to 100.0, and returns True if all sprites are scaled to 100.0.
	
		Parameters:
		all_sprites (list[ItemSprite]): The list of sprites to scale.
		scale_factor (float): The factor to scale the sprites by.
		stagger_animation (bool): Whether to stagger the animation by adding a delay.

		Returns:
		bool: True if all sprites are scaled to 1.0, False otherwise.
	
		Raises:
		ValueError: If scale_factor is negative.
	"""
		if scale_factor < 0:
			raise ValueError("scale_factor must be positive.")

		update_sprites_list = all_sprites

		if stagger_animation:
			update_sprites_list = [sprite for (i, sprite) in enumerate(all_sprites) if i == 0 or (i > 0 and all_sprites[i - 1].scale > 30)]
		
		if any(sprite.scale < 100 for sprite in update_sprites_list):
			self.scale_sprites(sprites=update_sprites_list, scale_factor=scale_factor, max_scale=100)
			return False

		pygame.time.delay(ANIMATION_DELAY)
		return True

	def scale_sprites(self, sprites: list[ItemSprite], scale_factor: float, max_scale: float = 100) -> None:
		""" Scales all sprites in the list by the given scaling factor up to the given max scale.

		Args:
		sprites (list[ItemSprite]): The list of sprites to scale.
		scale_factor (float): The factor to scale the sprites by.
		max_scale (float): The maximum scale of the sprites, beyond which the sprites will not scale.
		"""
		for sprite in sprites:
			# prevent scaling past the max scale
			new_scale_factor = scale_factor 
			if scale_factor + sprite.scale > max_scale:
				new_scale_factor = max_scale - sprite.scale

			self.animation_engine.add_animation(ScaleSprite(scaling_factor=new_scale_factor, sprite=sprite))
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
