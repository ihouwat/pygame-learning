import random

from config.types import Color, ItemCategory, ItemConfig, RealWorldObjectCategory, Shape, SpriteOption
from game_objects.models.puzzle import Puzzle


class ManyItemTypesPuzzle(Puzzle):
	""" Puzzle implementation for matching colored images."""

	@property
	def description(self) -> str:
		return'Match a colored image to a list of images'
	
	@property
	def option(self) -> SpriteOption:
		return None
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		return Puzzle.items()[ItemCategory.REAL_WORLD_OBJECTS]

class GrayscaleItemPuzzle(Puzzle):
	""" Puzzle implementation for matching grayscale images."""

	@property
	def description(self) -> str:
		return 'Match a grayscale image to a list of grayscale images'
	
	@property
	def option(self) -> SpriteOption:
		return SpriteOption.GRAYSCALE
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		return Puzzle.items()[ItemCategory.REAL_WORLD_OBJECTS]
	
class SpokenWordPuzzle(Puzzle):
	""" Puzzle implementation for matching spoken words."""
	
	@property
	def description(self) -> str:
		return 'Match a spoken word to a list of colored shapes'
	
	@property
	def option(self) -> SpriteOption:
		return SpriteOption.SPOKENWORD
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		return Puzzle.items()[ItemCategory.REAL_WORLD_OBJECTS]

class ColoredShapesPuzzle(Puzzle):
	""" Puzzle implementation for matching basic shapes with different colors."""

	@property
	def description(self) -> str:
		return 'Match a colored shape to a list of colored shapes'
	
	@property
	def option(self) -> SpriteOption:
		return SpriteOption.SHAPES
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		return Puzzle.items()[ItemCategory.SHAPES]

class ColorPuzzle(Puzzle):
	""" Puzzle implementation for matching shapes.""" 
	
	@property
	def description(self) -> str:
		return 'Match a colored shape to a list of shapes of various colors'
	
	@property
	def option(self) -> SpriteOption:
		return SpriteOption.SHAPES
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		random_shape = random.choice(list(Shape))
		return [x for x in Puzzle.items()[ItemCategory.SHAPES] if x.text_identifier == random_shape.value]

class ShapePuzzle(Puzzle):
	""" Puzzle implementation for matching shapes."""
	
	@property
	def description(self) -> str:
		return 'Match a colored shape to a list of shapes'
	
	@property
	def option(self) -> SpriteOption:
		return SpriteOption.SHAPES
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		color = random.choice(list(Color))
		return  [x for x in Puzzle.items()[ItemCategory.SHAPES] if x.color == color.value]

class SingleItemTypePuzzle(Puzzle):
	""" Puzzle implementation for matching a single type of item."""
	
	@property
	def description(self) -> str:
		return 'Match a colored item to a list of items of the same type'
	
	@property
	def option(self) -> SpriteOption:
		return None
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		type = random.choice([type for type in list(RealWorldObjectCategory)])
		return  [x for x in Puzzle.items()[ItemCategory.REAL_WORLD_OBJECTS] if x.type == type]
