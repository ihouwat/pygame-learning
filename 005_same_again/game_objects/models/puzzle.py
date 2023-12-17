
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from config.interfaces import GameItemConfig, GameObjectType
from config.game_items import game_items
from game_objects.models.item import SpriteOption
from engine.sprite_handler import SpriteHandler
from pygame.sprite import Group, Sprite


@dataclass(frozen=True, kw_only=True)
class Puzzle(ABC):
  """ 
    Represents a puzzle that can be played in the game.
    
    Attributes:
    items(dict[GameObjectType, GameItemConfig]): A dictionary of items to be used in the puzzle.
    description(str): A description of the puzzle.
    option(Option): An option to be applied to the puzzle.
    max_number_of_items(int): The maximum number of items to be used in the puzzle.
    puzzle_options(list[GameItemConfig]): A filtered list of options to construct the puzzle.
    """

  @classmethod
  def items(self) -> dict[GameObjectType, GameItemConfig]:
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
  def puzzle_options(self) -> list[GameItemConfig]:
    pass

  def generate(self) -> Tuple[Sprite, Group]:
    """ Generates a new puzzle."""
    new_group = SpriteHandler.create_sprite_group(max_number=self.max_number_of_items, items=self.puzzle_options, option=self.option)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    return item_to_match, new_group
