from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from engine.sprite_handler import SpriteHandler
from game_objects.entities.item import Item
from game_objects.game_items import game_items
from models.game_types import (
	ItemCategory,
	ItemConfig,
	SpriteOption,
)
from pygame import Surface
from pygame.sprite import Group


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
	item_to_match: Item = Item(image=Surface((0, 0)), word="", text_identifier="")
	
	@classmethod
	def item_catalog(cls) -> dict[ItemCategory, list[ItemConfig]]:
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

	def generate(self) -> Tuple[Item, Group]:
		""" Generates a new puzzle."""
		self.items = SpriteHandler.create_sprite_group(max_number=self.max_number_of_items, item_configs=self.puzzle_options, option=self.option)
		self.item_to_match = SpriteHandler.pick_item_to_match(self.items)
		return self.item_to_match, self.items
