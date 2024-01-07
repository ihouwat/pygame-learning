from engine.animation_engine import AnimationEngine
from game_objects.item_sprite import ItemSprite
from engine.animations import ScaleSprite


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
  """
		if any(sprite.scale > 0 for sprite in all_sprites):
			for sprite in all_sprites:
				self.animation_engine.add_animation(ScaleSprite(scaling_factor=scale_factor, sprite=sprite))
			self.animation_engine.execute()
			return False
		return True