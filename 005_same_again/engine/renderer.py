import pygame
from config.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from game_objects.entities.level import Level
from game_objects.entities.status_bar import StatusBar
from pygame.sprite import Group, Sprite


class Renderer:
  """ Handles the rendering of the game."""
  def __init__(self):
    self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Same Again")

  def draw(self, level: Level, status_bar: StatusBar) -> None:
    """ Updates the screen with a new set of items and a target item."""
    self.arrange_items(level.puzzle.items)
    self.draw_items(level.puzzle.items, level.puzzle.item_to_match)
    self.draw_status_bar(status_bar, level.score, level.level_number)

  def arrange_items(self, items: Group) -> None:
    """ Arranges a group of items on the screen. """
    total_items_width = sum(item.rect.width for item in items)
    # subtract total items width from screen width and divide by number of items + 1 to distribute spacing evenly between items
    spacing = (SCREEN_WIDTH - total_items_width) / (len(items) + 1)
    x = spacing
    y = SCREEN_HEIGHT - 300

    for item in items:
      item.update_rect(x, y)
      x += item.rect.width + spacing

  def draw_items(self, items: Group, item_to_match: Sprite) -> None:
    """ Renders the screen with a new set of items, a target item."""
    self.display_surface.fill((0, 0, 0))
    self.display_surface.blit(item_to_match.image, ((SCREEN_WIDTH / 2) - (item_to_match.rect.width / 2), 100))
    for sprite in items:
      self.display_surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
    
  def draw_status_bar(self, status_bar: StatusBar, score: int, level: int) -> None:
    """ Renders the status bar."""
    for surface, position in status_bar.update(score, level):
      self.display_surface.blit(surface, position)