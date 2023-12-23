
import os
import pathlib
import sys

import pygame


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
