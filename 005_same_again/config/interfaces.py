
from enum import Enum
from typing import NamedTuple

import pygame


class Color(Enum):
  RED = 'Red'
  GREEN = 'Green'
  BLUE = 'Blue'
  YELLOW = 'Yellow'
  WHITE = 'White'

class ItemType(Enum):
  FRUIT = 'Fruit'
  SHAPE = 'Shape'

class GameItemConfig(NamedTuple):
  text_identifier: str
  image: str | pygame.Surface
  sound: str
  word: str
  color: Color
  type: ItemType

class GameObjectType(Enum):
  ITEMS = 'Items'
  SHAPES = 'Shapes'

class Shape(Enum):
  CIRCLE = 'Circle'
  SQUARE = 'Square'
  TRIANGLE = 'Triangle',
  RECTANGLE = 'Rectangle'

class SpriteOption(Enum):
  """ Represents an option to be applied to a sprite."""
  GRAYSCALE = 'Grayscale'
  SHAPES = 'Shapes',
  SPOKENWORD = 'Spokenword'
