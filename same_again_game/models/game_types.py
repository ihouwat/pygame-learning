
from enum import Enum


class Color(Enum):
  RED = 'Red'
  GREEN = 'Green'
  BLUE = 'Blue'
  YELLOW = 'Yellow'
  WHITE = 'White'
  ORANGE = 'Orange'
  PURPLE = 'Purple'
  BROWN = 'Brown',
  PINK = 'Pink',
  GREY = 'Grey',
  BLACK = 'Black'

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
  VEGETABLE = 'Vegetable'
  ANIMAL = 'Animal'
  VEHICLE = 'Vehicle'

class Shape(Enum):
  """ Represents a shape to construct a sprite with."""
  CIRCLE = 'Circle'
  SQUARE = 'Square'
  TRIANGLE = 'Triangle'
  RECTANGLE = 'Rectangle'

class SpriteOption(Enum):
  """ Represents an option to be applied to a sprite."""
  NONE = 'None'
  GRAYSCALE = 'Grayscale'
  SHAPES = 'Shapes',
  SPOKENWORD = 'Spoken word'

class GameAction(Enum):
  """ Represents an action to be applied in response to an event."""
  START_NEW_GAME = 0
  QUIT = 1
  ITEM_SELECTED = 2
  MATCH_DETECTED = 3
  OPEN_MENU = 4
  RESUME_GAME = 5
  MOUSE_ENTERED_WINDOW = 6
  MOUSE_EXITED_WINDOW = 7

class GameState(Enum):
  """ State machine for the game."""
  PLAYING = 1
  MENU_IS_OPEN = 2
  LEVEL_COMPLETED = 3
  GAME_COMPLETED = 4
  PAUSED = 5
  TRANSITION_TO_NEXT_TURN = 6
  TRANSITION_TO_NEXT_LEVEL = 7
  START_NEW_TURN = 8

class ProcessPointResult(Enum):
  """ Represents the result of processing a point gain."""
  LEVEL_COMPLETED = 1
  TURN_COMPLETED = 2

class TextElementType(Enum):
  LEVEL_UP = 1
  GAME_COMPLETED = 2

class Language(Enum):
  """ Represents a language to be used in the game."""
  ENGLISH = "English"
  ARABIC = "Arabic"
  PORTUGUESE = "Portuguese"
  
class SoundType(Enum):
  INTRO = 1
  GAME_MUSIC = 2
  EFFECTS = 3
  
Soundtracks = dict[SoundType, list[str]]
