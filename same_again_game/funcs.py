
import os
import pathlib
import sys

import pygame

from config.settings import SHAPE_HEIGHT, SHAPE_WIDTH
from models.game_types import Shape


def get_file(*path_args) -> str:
  """
  Get the absolute file path starting from the root of the package.

  Args:
    *path_args: Variable number of path arguments to be joined.

  Returns:
    str: The absolute file path.
  """
  # sys.modules['__main__'].__file__ is how we get the path to the main module
  if sys.modules['__main__'].__file__ is not None:
    package_root = pathlib.Path(sys.modules['__main__'].__file__).resolve().parent
    file_path = os.path.join(package_root, *path_args)
    return file_path
  else:
    raise RuntimeError("Unable to find the main module. The main module is required for the application to run correctly.")

def load_pygame_image(*path_args) -> pygame.Surface:
  """
  Load an image using pygame and return it as a pygame.Surface object.
  Args:
    *path_args: Variable number of string arguments representing the path to the image file.
  
  Returns:
    pygame.Surface: The loaded image as a pygame.Surface object.
  """
  file_path = get_file(*path_args)
  return pygame.image.load(file_path).convert_alpha()


def create_shape(shape: Shape, color: tuple[int, int, int], width: float = SHAPE_WIDTH, height: float = SHAPE_HEIGHT) -> pygame.Surface:
  """ Creates a surface with a shape drawn on it.
  
  Args:
    shape (Shape): The shape to draw.
    color (tuple[int, int, int]): The color of the shape.
    width (float): The width of the surface.
    height (float): The height of the surface.
    
  Returns:
    pygame.Surface: The surface with the shape drawn on it.
    
  Raises:
    ValueError: If either width or height are negative.
  """
  if width < 0 or height < 0:
        raise ValueError("Width and height must be non-negative")

  surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface with alpha channel

  if shape == Shape.CIRCLE:
    pygame.draw.circle(surface=surface, color=color, center=(width // 2, height // 2), radius=min(width, height) // 2)
  elif shape == Shape.SQUARE:
    pygame.draw.rect(surface=surface, color=color, rect=(0, 0, width, height))
  elif shape == Shape.TRIANGLE:
    pygame.draw.polygon(surface=surface, color=color, points=[(width // 2, 0), (0, height), (width, height)])
  elif shape == Shape.RECTANGLE:
    pygame.draw.rect(surface=surface, color=color, rect=(0, height // 4, width, height // 2))

  return surface