import pygame


class TextElement:
	def __init__(self, text: str, font: pygame.font.Font, color: pygame.Color, x: int, y: int):
		self.text: str = text
		self.font: pygame.font.Font = font
		self.color: pygame.Color = color
		self.start_position: tuple[int, int] = (x, y)
		self.current_position: tuple[int, int] = (x, y)
		self.surface: pygame.Surface = self.font.render(self.text, True, self.color)
	
	def set_text(self, text: str) -> None:
		self.text = text
		self.surface = self.font.render(self.text, True, self.color)
	
	def set_position(self, x: int, y: int) -> None:
		self.current_position = (x, y)
	
	def reset_to_start_position(self) -> None:
		self.current_position = self.start_position
	
	def draw(self) -> pygame.Surface:
		return self.surface
