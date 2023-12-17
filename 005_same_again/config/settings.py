from config.interfaces import Color

# Predefined color values
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

colors = {
  Color.RED: RED,
  Color.GREEN: GREEN,
  Color.BLUE: BLUE, 
  Color.YELLOW: YELLOW,
  Color.WHITE: WHITE
}

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Frames per second
FPS = 30
