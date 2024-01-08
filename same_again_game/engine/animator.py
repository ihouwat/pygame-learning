import pygame
from config.settings import ANIMATION_DELAY
from engine.animation_engine import AnimationEngine
from engine.animations import ScaleSprite
from game_objects.item_sprite import ItemSprite


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