import pygame


class TextElement:
	def __init__(self, text: str, font: pygame.font.Font, color: pygame.Color, x: int, y: int):
		self.text = text
		self.font = font
		self.color = color
		self.start_position = (x, y)
		self.current_position = (x, y)
	
	def set_text(self, text: str) -> None:
		self.text = text
	
	def set_position(self, x: int, y: int) -> None:
		self.current_position = (x, y)
	
	def draw(self) -> pygame.Surface:
		return self.font.render(self.text, True, self.color)
