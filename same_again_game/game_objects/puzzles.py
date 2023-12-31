import random

from config.settings import colors
from models.game_types import (
	ItemCategory,
	RealWorldObjectCategory,
	Shape,
	SpriteOption,
)
from models.item_config import ItemConfig
from models.puzzle import Puzzle


class ManyItemTypesPuzzle(Puzzle):
	""" Puzzle implementation for matching colored images."""

	@property
	def description(self) -> str:
		return'Match a colored image to a list of images'
	
	@property
	def option(self) -> SpriteOption:
		return SpriteOption.NONE
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		return Puzzle.item_catalog()[ItemCategory.REAL_WORLD_OBJECTS]

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
		return Puzzle.item_catalog()[ItemCategory.REAL_WORLD_OBJECTS]
	
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
		return Puzzle.item_catalog()[ItemCategory.REAL_WORLD_OBJECTS]

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
		return Puzzle.item_catalog()[ItemCategory.SHAPES]

class ColorPuzzle(Puzzle):
	""" Puzzle implementation for matching shapes.

	Attributes:
		random_shape: The shape to be selected throughout the duration of the puzzle.
  """
	random_shape = random.choice(list(Shape))

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
		return [x for x in Puzzle.item_catalog()[ItemCategory.SHAPES] if x.text_identifier == self.random_shape.value]

class ShapePuzzle(Puzzle):
	""" Puzzle implementation for matching shapes.

	Attributes:
		color: The color to be applied to the shapes throughout the duration of the puzzle.
	"""
	
	color = random.choice(list(colors.keys()))

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
		return  [x for x in Puzzle.item_catalog()[ItemCategory.SHAPES] if x.color == self.color]

class SingleItemTypePuzzle(Puzzle):
	""" Puzzle implementation for matching a single type of item.

	Attributes:
		type: The type of item to be matched throughout the duration of the puzzle.
	"""
	type: RealWorldObjectCategory = random.choice(list(RealWorldObjectCategory))
	
	@property
	def description(self) -> str:
		return 'Match a colored item to a list of items of the same type'
	
	@property
	def option(self) -> SpriteOption:
		return SpriteOption.NONE
	
	@property
	def max_number_of_items(self) -> int:
		return 4
	
	@property
	def puzzle_options(self) -> list[ItemConfig]:
		return [x for x in Puzzle.item_catalog()[ItemCategory.REAL_WORLD_OBJECTS] if x.type == self.type]
