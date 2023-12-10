
import os
import pathlib
import sys

import pygame

def get_file(*path_args) -> str:
  """
  Get the absolute file path

  Args:
    *path_args: Variable number of path arguments to be joined.

  Returns:
    str: The absolute file path.
  """
  file_path = os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), *path_args)
  return file_path

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

# PERHAPS MOVE TO SOME MANAGER CLASS
def quit_game():
  """
  Quits game and exits program.
  """
  pygame.quit()
  sys.exit()