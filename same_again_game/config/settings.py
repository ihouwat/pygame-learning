import pygame
from models.game_types import Color

# Predefined color values
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)

colors: dict[Color, tuple[int, int, int]] = {
  Color.RED: RED,
  Color.GREEN: GREEN,
  Color.BLUE: BLUE, 
  Color.YELLOW: YELLOW,
  Color.WHITE: WHITE,
  Color.ORANGE: ORANGE,
  Color.PURPLE: PURPLE,
  Color.PINK: PINK
}

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

SHAPE_WIDTH = 140
SHAPE_HEIGHT = 140

# Time settings
FPS = 60
ANIMATION_DELAY = 250

# Fonts
FONT_NAME = "Verdana"
FONT_REGULAR = 60
FONT_SMALL = 20
FONT_LARGE = 120

# Custom events
START_GAME = pygame.USEREVENT
RESUME_GAME = pygame.USEREVENT + 1