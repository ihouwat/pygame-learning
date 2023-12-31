import pygame
from config.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from game_objects.item_sprite import ItemSprite
from game_objects.text_element import TextElement
from models.game_types import GameState, TextElementType
from pygame.sprite import Group
from ui.game_menu import GameMenu
from ui.status_bar import StatusBar
from ui.ui_display import UIDisplay


class Renderer:
	""" Handles the rendering of the game.
	This class is reponsible for both laying out the game objects on the screen and rendering them.
	That's ok considering the simplicity of the game.
	
	Attributes:
		display_surface(pygame.Surface): The surface to be rendered.
	"""
	def __init__(self):
		self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Same Again")

	def draw(self, item_to_match: ItemSprite, items: Group, status_bar: StatusBar, ui_display: UIDisplay, game_menu: GameMenu, game_state: GameState, text_elements: dict[TextElementType, TextElement]) -> None:
		""" Layouts and updates the screen with a new set of items, a target item, and updates status bar.
  
		Args:
			item_to_match (ItemSprite): The target item.
			items (Group): The group of items to be displayed.
			status_bar (StatusBar): The status bar to be displayed.
			ui_display (UIDisplay): The ui elements to be displayed.
			game_menu (GameMenu): The game menu to be displayed.
			game_state (GameState): The current game state to dictate what to render.
			text_elements (dict[TextElementType, TextElement]): Dictionary of text elements to be displayed based on game state.
		"""
		self.draw_background()

		if game_menu.menu.is_enabled() and game_state == GameState.MENU_IS_OPEN:
			self.draw_game_menu(game_menu)
			return
		if game_state == GameState.TRANSITION_TO_NEXT_LEVEL:
			self.render_text(text_element=text_elements[TextElementType.LEVEL_UP])
			return
		if game_state == GameState.GAME_COMPLETED:
			self.render_text(text_element=text_elements[TextElementType.GAME_COMPLETED])
			return
		else:
			# Layout
			self.layout_items(items)
			self.layout_item_to_match(item_to_match)
			# Render
			self.draw_items(items, item_to_match)
			self.draw_status_bar(status_bar, ui_display)

	def layout_items(self, items: Group) -> None:
		""" Arranges a group of items on the screen.
		
		Args:
			items (Group): The group of items to be arranged.
		
		"""
		total_items_width = sum(item.rect.width for item in items)
		# subtract total items width from screen width and divide by number of items + 1 to distribute spacing evenly between items
		spacing = (SCREEN_WIDTH - total_items_width) / (len(items) + 1)
		x = spacing
		y = SCREEN_HEIGHT - 300

		for item in items:
			item.update(x, y)
			x += item.rect.width + spacing

	def layout_item_to_match(self, item_to_match: ItemSprite) -> None:
		""" Arranges the target item on the screen.

		Args:
			item_to_match (ItemSprite): The target item to be arranged.
		"""
		item_to_match.update((SCREEN_WIDTH // 2) - (item_to_match.rect.width // 2), 100)

	def draw_items(self, items: Group, item_to_match: ItemSprite) -> None:
		""" Renders the screen with a new set of items and a target item.
		
		Args:
			items (Group): The group of items to be displayed.
			item_to_match (ItemSprite): The target item to be displayed.
    """
		self.display_surface.blit(item_to_match.image, (item_to_match.rect.x, item_to_match.rect.y))
		for sprite in items:
			self.display_surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
			
	def draw_background(self) -> None:
		""" Renders the background."""
		self.display_surface.fill((0, 0, 0))
		
	def draw_status_bar(self, status_bar: StatusBar, ui_display: UIDisplay) -> None:
		""" Renders the status bar.
		
		Args:
			status_bar (StatusBar): The status bar to be displayed.
			ui_display (UIDisplay): The ui elements to be displayed.
		"""
		for surface, position in status_bar.update(ui_display=ui_display):
			self.display_surface.blit(surface, position)
			
	def draw_game_menu(self, game_menu: GameMenu) -> None:
		""" Renders the game menu.
		
		Args:
			game_menu (GameMenu): The game menu object to be displayed.
		"""
		game_menu.menu.draw(self.display_surface)
	
	def render_text(self, text_element: TextElement) -> None:
		""" Renders text elements.
	
		Args:
			text_element (TextElement): The text element to be rendered.
		"""
		self.display_surface.blit(text_element.draw(), text_element.current_position)