
from enum import Enum
from typing import NamedTuple
import pygame
from config.settings import BLUE, GREEN, RED, WHITE, YELLOW

class Color(Enum):
  RED = 'Red'
  GREEN = 'Green'
  BLUE = 'Blue'
  YELLOW = 'Yellow'
  WHITE = 'White'

colors = {
  Color.RED: RED,
  Color.GREEN: GREEN,
  Color.BLUE: BLUE, 
  Color.YELLOW: YELLOW,
  Color.WHITE: WHITE
}

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
