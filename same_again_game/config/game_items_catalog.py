import pygame
from config.settings import colors
from models.game_types import (
  Color,
  ItemCategory,
  ItemConfig,
  RealWorldObjectCategory,
  Shape,
)
from models.image_source import PathSource, SurfaceSource

""" Game items will be used to create sprites for the puzzles that will be used in the game. 
  There are two types of game items:
    1. Items: A sprite that represents an object from an image.
    2. Shapes: A sprite that represents a shape drawn with the Pygame API.
"""

# game_items: list[Item] = [Item(**x) for x in [
# 	{"text_identifier": "banana", "image": "img", "sound": "mp3", "word": "Banana"},
# 	{"text_identifier": "apple", "image": "img", "sound": "mp3", "word": "Apple"},
# 	{"text_identifier": "orange", "image": "img", "sound": "mp3", "word": "Orange"},
# 	{"text_identifier": "pear", "image": "img", "sound": "mp3", "word": "Pear"},
# 	{"text_identifier": "grapes", "image": "img", "sound": "mp3", "word": "Grapes"},
# 	{"text_identifier": "strawberry", "image": "img", "sound": "mp3", "word": "Strawberry"},
# 	{"text_identifier": "pineapple", "image": "img", "sound": "mp3", "word": "Pineapple"},
# 	{"text_identifier": "watermelon", "image": "img", "sound": "mp3", "word": "Watermelon"},

# 	{"text_identifier": "carrot", "image": "img", "sound": "mp3", "word": "A carrot"},
# 	{"text_identifier": "potato", "image": "img", "sound": "mp3", "word": "A potato"},
# 	{"text_identifier": "onion", "image": "img", "sound": "mp3", "word": "An onion"},
# 	{"text_identifier": "tomato", "image": "img", "sound": "mp3", "word": "A tomato"},
# 	{"text_identifier": "cucumber", "image": "img", "sound": "mp3", "word": "A cucumber"},
# 	{"text_identifier": "pepper", "image": "img", "sound": "mp3", "word": "A pepper"},
# 	{"text_identifier": "broccoli", "image": "img", "sound": "mp3", "word": "Broccoli"},
# 	{"text_identifier": "lettuce", "image": "img", "sound": "mp3", "word": "Lettuce"},
# 	{"text_identifier": "mushroom", "image": "img", "sound": "mp3", "word": "A mushroom"},
# 	{"text_identifier": "corn", "image": "img", "sound": "mp3", "word": "Corn"},


# 	{"text_identifier": "chair", "image": "img", "sound": "mp3", "word": "A chair"},
# 	{"text_identifier": "table", "image": "img", "sound": "mp3", "word": "A table"},
# 	{"text_identifier": "couch", "image": "img", "sound": "mp3", "word": "A couch"},
# 	{"text_identifier": "bed", "image": "img", "sound": "mp3", "word": "A bed"},
# 	{"text_identifier": "lamp", "image": "img", "sound": "mp3", "word": "A lamp"},
# 	{"text_identifier": "television", "image": "img", "sound": "mp3", "word": "A television"},
# 	{"text_identifier": "computer", "image": "img", "sound": "mp3", "word": "A computer"},
# 	{"text_identifier": "refrigerator", "image": "img", "sound": "mp3", "word": "A refrigerator"},
# 	{"text_identifier": "microwave", "image": "img", "sound": "mp3", "word": "A microwave"},
# 	{"text_identifier": "toaster", "image": "img", "sound": "mp3", "word": "A toaster"},

# 	{"text_identifier": "dog", "image": "img", "sound": "mp3", "word": "A dog"},
# 	{"text_identifier": "cat", "image": "img", "sound": "mp3", "word": "A cat"},
# 	{"text_identifier": "bird", "image": "img", "sound": "mp3", "word": "A bird"},
# 	{"text_identifier": "fish", "image": "img", "sound": "mp3", "word": "A fish"},
# 	{"text_identifier": "rabbit", "image": "img", "sound": "mp3", "word": "A rabbit"},
# 	{"text_identifier": "hamster", "image": "img", "sound": "mp3", "word": "A hamster"},
# 	{"text_identifier": "horse", "image": "img", "sound": "mp3", "word": "A horse"},
# 	{"text_identifier": "turtle", "image": "img", "sound": "mp3", "word": "A turtle"},
# 	{"text_identifier": "snake", "image": "img", "sound": "mp3", "word": "A snake"},
# 	{"text_identifier": "frog", "image": "img", "sound": "mp3", "word": "A frog"},
# ]]

items_config: list[ItemConfig] = [
  ItemConfig(**x)
  for x in [
    {"text_identifier": "banana", "image": PathSource("banana.png"), "sound": "mp3", "word": "Banana", "color": Color.YELLOW, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "strawberry", "image": PathSource("strawberry.png"), "sound": "mp3", "word": "Strawberry", "color": Color.RED, "type":RealWorldObjectCategory.FRUIT},
    {"text_identifier": "pear", "image": PathSource("pear.png"), "sound": "mp3", "word": "Pear", "color": Color.RED, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "apple", "image": PathSource("apple.png"), "sound": "mp3", "word": "Apple", "color": Color.GREEN, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "pineapple", "image": PathSource("pineapple.png"), "sound": "mp3", "word": "Pineapple", "color": Color.YELLOW, "type": RealWorldObjectCategory.FRUIT},
  ]
]

def create_shape(shape: Shape, color: tuple[int, int, int]) -> pygame.Surface:
  """ Creates a surface with a shape drawn on it."""
  width = 140
  height = 140
  surface = pygame.Surface((width, height))

  if shape == Shape.CIRCLE:
    pygame.draw.circle(surface=surface, color=color, center=(width // 2, height // 2), radius=width/2)
  elif shape == Shape.SQUARE:
    pygame.draw.rect(surface=surface, color=color, rect=(0, 0, width, width))
  elif shape == Shape.TRIANGLE:
    pygame.draw.polygon(surface=surface, color=color, points=[(width // 2, 0), (0, height), (width, height)])
  elif shape == Shape.RECTANGLE:
    pygame.draw.rect(surface=surface, color=color, rect=(0, height // 4, width, height // 2))

  return surface

shapes_config: list[ItemConfig] = [
  ItemConfig(
        text_identifier=str(shape.value),
        image=SurfaceSource(create_shape(shape, color_value)),
        sound=str(shape.value),
        word=str(shape.value),
        color=color_name,
        type="Shape"
    )
  for shape in Shape
  for color_name, color_value in colors.items()
]
game_items_catalog: dict[ItemCategory, list[ItemConfig]] = {
  ItemCategory.REAL_WORLD_OBJECTS: items_config,
  ItemCategory.SHAPES: shapes_config
}
