import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

from config.types import (
	Color,
	ItemCategory,
	ItemConfig,
	RealWorldObjectCategory,
	Shape,
	SpriteOption,
)
from engine.sprite_handler import SpriteHandler
from game_objects.game_items import game_items
from pygame.sprite import Group, Sprite


@dataclass(kw_only=True)
class Puzzle(ABC):
	""" 
		Represents a puzzle that can be played in the game.
		
		Attributes:
		items(Group): A group of items to be used in the puzzle.
		item_to_match(Sprite): The item that the player needs to match.
		item_catalog(dict[ItemCategory, ItemConfig]): A dictionary of items to be used in the puzzle.
		description(str): A description of the puzzle.
		option(Option): An option to be applied to the puzzle.
		max_number_of_items(int): The maximum number of items to be used in the puzzle.
		puzzle_options(list[ItemConfig]): A filtered list of options to construct the puzzle.
		"""
	
	items: Group = Group()
	item_to_match: Sprite = Sprite()
	
	@classmethod
	def item_catalog(self) -> dict[ItemCategory, ItemConfig]:
		return game_items

	@property
	@abstractmethod
	def description(self) -> str:
		pass
	
	@property
	@abstractmethod
	def option(self) -> SpriteOption:
		pass
	
	@property
	@abstractmethod
	def max_number_of_items(self) -> int:
		pass
	
	@property
	@abstractmethod
	def puzzle_options(self) -> list[ItemConfig]:
		pass

	def generate(self) -> Tuple[Sprite, Group]:
		""" Generates a new puzzle."""
		self.items = SpriteHandler.create_sprite_group(max_number=self.max_number_of_items, items=self.puzzle_options, option=self.option)
		self.item_to_match = SpriteHandler.pick_item_to_match(self.items)
		return self.item_to_match, self.items

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
		return [x for x in Puzzle.item_catalog()[ItemCategory.SHAPES] if x.text_identifier == random_shape.value]

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
		return  [x for x in Puzzle.item_catalog()[ItemCategory.SHAPES] if x.color == color.value]

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
		return  [x for x in Puzzle.item_catalog()[ItemCategory.REAL_WORLD_OBJECTS] if x.type == type]
