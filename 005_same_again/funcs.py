
import os
import pathlib
import sys

import pygame

def get_file(*path_args) -> str:
	file_path = os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), *path_args)
	return file_path

def load_pygame_image(*path_args) -> pygame.Surface:
  file_path = get_file(*path_args)
  return pygame.image.load(file_path).convert_alpha()

# PERHAPS MOVE TO SOME MANAGER CLASS
def quit_game():
    pygame.quit()
    sys.exit()