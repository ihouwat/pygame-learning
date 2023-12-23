
from enum import Enum
from typing import NamedTuple

from models.image_content import ImageSource


class Color(Enum):
  RED = 'Red'
  GREEN = 'Green'
  BLUE = 'Blue'
  YELLOW = 'Yellow'
  WHITE = 'White'

class ItemCategory(Enum):
  """ Represents the category of item to be created.
    Real-world objects: images that represent real-world objects, such as fruits, vegetables, vehicles, household items, etc.
    Shapes: a shape drawn with the Pygame API.
  """
  REAL_WORLD_OBJECTS = 'Real-world objects'
  SHAPES = 'Shapes'

class RealWorldObjectCategory(Enum):
  """ Represents the type of item to be created."""
  FRUIT = 'Fruit'

class ItemConfig(NamedTuple):
  """ Represents metadata for items that are the basis to create sprites."""
  text_identifier: str
  image: ImageSource
  sound: str
  word: str
  color: Color
  type: RealWorldObjectCategory | str

class Shape(Enum):
  """ Represents a shape to construct a sprite with."""
  CIRCLE = 'Circle'
  SQUARE = 'Square'
  TRIANGLE = 'Triangle',
  RECTANGLE = 'Rectangle'

class SpriteOption(Enum):
  """ Represents an option to be applied to a sprite."""
  NONE = 'None'
  GRAYSCALE = 'Grayscale'
  SHAPES = 'Shapes',
  SPOKENWORD = 'Spokenword'

class GameAction(Enum):
  """ Represents an action to be applied in response to an event."""
  START_GAME = 0,
  QUIT = 1,
  OBJECT_SELECTED = 2,

class Language(Enum):
  """ Represents a language to be used in the game."""
  ENGLISH = "English"
  ARABIC = "Arabic"
  PORTUGUESE = "Portuguese"