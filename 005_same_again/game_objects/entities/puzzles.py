import random

from config.interfaces import Color, GameObjectType, ItemType, Shape, SpriteOption
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
	def puzzle_options(self) -> GameObjectType:
		return Puzzle.items()[GameObjectType.ITEMS]

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
	def puzzle_options(self) -> GameObjectType:
		return Puzzle.items()[GameObjectType.ITEMS]
	
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
	def puzzle_options(self) -> GameObjectType:
		return Puzzle.items()[GameObjectType.ITEMS]

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
	def puzzle_options(self) -> GameObjectType:
		return Puzzle.items()[GameObjectType.SHAPES]

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
	def puzzle_options(self) -> GameObjectType:
		random_shape = random.choice(list(Shape))
		return [x for x in Puzzle.items()[GameObjectType.SHAPES] if x.text_identifier == random_shape.value]

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
	def puzzle_options(self) -> GameObjectType:
		color = random.choice(list(Color))
		return  [x for x in Puzzle.items()[GameObjectType.SHAPES] if x.color == color.value]

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
	def puzzle_options(self) -> GameObjectType:
		type = random.choice([type for type in list(ItemType) if type != ItemType.SHAPE])
		return  [x for x in Puzzle.items()[GameObjectType.ITEMS] if x.type == type]
