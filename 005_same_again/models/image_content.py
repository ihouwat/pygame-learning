import pygame
from funcs import load_pygame_image


class ImageSource():
	def get_image(self) -> pygame.Surface:
		raise NotImplementedError

class SurfaceSource(ImageSource):
	def __init__(self, surface: pygame.Surface):
		self.surface = surface

	def get_image(self):
		return self.surface

class PathSource(ImageSource):
	def __init__(self, path: str):
		self.path = path

	def get_image(self):
		return load_pygame_image('assets', 'images', self.path)