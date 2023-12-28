
from engine.animations import Animation


class AnimationEngine:
	""" AnimationEngine is responsible for updating all animations in the game. 
	
	Attributes:
		animations: A list of all animations that can be executed.
	"""
	def __init__(self):
		self.animations = []

	def add_animation(self, animation: Animation) -> "AnimationEngine":
		self.animations.append(animation)
		return self

	def execute(self):
		while any(not animation.is_finished for animation in self.animations):
			for animation in self.animations:
				animation.update()
				if animation.is_finished:
					self.animations.remove(animation)
