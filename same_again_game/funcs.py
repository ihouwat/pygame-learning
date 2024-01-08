
import os
import pathlib
import sys

import pygame
from config.settings import (
  MUSIC_PATH,
  SHAPE_HEIGHT,
  SHAPE_WIDTH,
  SOUND_EFFECTS_PATH,
  SPOKEN_WORD_PATH,
)
from models.game_types import Shape, RGB


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

def load_pygame_sound(*path_args) -> pygame.mixer.Sound:
  """
  Load a sound using pygame and return it as a pygame.mixer.Sound object.
  Args:
    *path_args: Variable number of string arguments representing the path to the sound file.
  
  Returns:
    pygame.mixer.Sound: The loaded sound as a pygame.mixer.Sound object.
  """
  file_path = get_file(*path_args)
  return pygame.mixer.Sound(file_path)

def get_music_track_path(track_name: str) -> str:
  """ Get the absolute file path for a music track.
  
  Args:
    track_name (str): The name of the track, including the file extension.
    
  Returns:
    str: The absolute file path for the track.
  """
  return get_file(*MUSIC_PATH, track_name)

def get_sound_effect_path(sound_effect_name: str) -> str:
  """ Get the absolute file path for a sound effect.
  
  Args:
    sound_effect_name (str): The name of the sound effect, including the file extension.
    
  Returns:
    str: The absolute file path for the sound effect.
  """
  return get_file(*SOUND_EFFECTS_PATH, sound_effect_name)

def get_spoken_word_path(language: str, word: str) -> str:
  """ Get the absolute file path for a spoken word.
  
  Args:
    language (str): The language of the spoken word
    word (str): The word, including the file extension.
    
  Returns:
    str: The absolute file path for the spoken word.
  """
  return get_file(*SPOKEN_WORD_PATH, language, word)

def create_shape(shape: Shape, color: RGB, width: float = SHAPE_WIDTH, height: float = SHAPE_HEIGHT) -> pygame.Surface:
  """ Creates a surface with a shape drawn on it.
  
  Args:
    shape (Shape): The shape to draw.
    color (RGB): The color of the shape in RGB format.
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