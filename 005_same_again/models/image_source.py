from typing import Protocol

import pygame
from funcs import load_pygame_image


class ImageSource(Protocol):
	""" Represents a source for an image."""

	def get_image(self) -> pygame.Surface:
		raise NotImplementedError

class SurfaceSource(ImageSource):
	""" Represents a source for an image that is a pygame surface.
	
	Attributes:
		surface(pygame.Surface): The image of the item.
	"""
	def __init__(self, surface: pygame.Surface):
		self.surface = surface

	def get_image(self):
		return self.surface

class PathSource(ImageSource):
	""" Represents a source for an image that is a path.

	Attributes:
		path(str): The path to the image.
	"""
	def __init__(self, path: str):
		self.path = path

	def get_image(self):
		return load_pygame_image('assets', 'images', self.path)