
from engine.animations import Animation


class AnimationEngine:
	""" AnimationEngine is responsible for updating all animations in the game. 
	
	Attributes:
		animations(Animation): A list of all animations that can be executed.
	"""
	def __init__(self):
		self.animations = []

	def add_animation(self, animation: Animation) -> "AnimationEngine":
		""" Adds an animation to the list of animations that can be executed.

		Args:
			animation (Animation): The animation to add.
		Returns:
			AnimationEngine: The AnimationEngine instance.
	"""
		self.animations.append(animation)
		return self

	def execute(self):
		""" Executes all animations in the animations list. """
		while any(not animation.is_finished for animation in self.animations):
			for animation in self.animations:
				animation.update()
				if animation.is_finished:
					self.animations.remove(animation)
