
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
  """ Represents the type of item to be created."""
  FRUIT = 'Fruit'
  SHAPE = 'Shape'

class GameItemConfig(NamedTuple):
  """ Represents metadata for items that are the basis to create sprites."""
  text_identifier: str
  image: str | pygame.Surface
  sound: str
  word: str
  color: Color
  type: ItemType

class GameObjectType(Enum):
  """ Represents the type of sprite to be created.
    Items: A sprite that represents an object from an image.
    Shapes: A sprite that represents a shape drawn with the Pygame API.
  """
  ITEMS = 'Items'
  SHAPES = 'Shapes'

class Shape(Enum):
  """ Represents a shape to construct a sprite with."""
  CIRCLE = 'Circle'
  SQUARE = 'Square'
  TRIANGLE = 'Triangle',
  RECTANGLE = 'Rectangle'

class SpriteOption(Enum):
  """ Represents an option to be applied to a sprite."""
  GRAYSCALE = 'Grayscale'
  SHAPES = 'Shapes',
  SPOKENWORD = 'Spokenword'
