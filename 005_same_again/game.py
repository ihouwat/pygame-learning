
import sys

import pygame
from config.types import GameAction
from engine.event_handler import EventListener
from engine.renderer import Renderer
from engine.sprite_handler import SpriteHandler
from game_objects.entities.level import Level
from game_objects.entities.puzzles import Puzzle
from game_objects.entities.status_bar import StatusBar
from pygame.sprite import Group, Sprite


class Game:
  """ Represents a game of Same Again."""

  def __init__(self, renderer: Renderer, event_listener: EventListener, status_bar: StatusBar, levels: list[Puzzle]):
    self.renderer: Renderer = renderer
    self.event_listener: EventListener = event_listener
    self.status_bar: StatusBar = status_bar
    self.levels: list[Puzzle] = levels
    self.current_level: Level = self.levels[0]

    self.render_new_puzzle()

  def run(self, events: list[pygame.event.Event]) -> None:
    """ Primary method that runs the game."""
    action = self.event_listener.process_events(events)
    items = self.current_level.puzzle.items
    item_to_match = self.current_level.puzzle.item_to_match

    if action == GameAction.QUIT:
      self.quit()
    if action == GameAction.OBJECT_SELECTED:
      if(self.match_detected(items, item_to_match, pygame.mouse.get_pos())):
        self.process_point_gain()

  def match_detected(self, items: Group, item_to_match: Sprite, coordinates) -> bool:
    """ Returns True if a user has match an item correctly against a list of items, False otherwise.
    Args:
      items (Group): A group of items to match against.
      item_to_match (Sprite): The item to match.
      coordinates (tuple): The coordinates of the mouse click event.
    """
    selected_item = [sprite for sprite in items if sprite.rect.collidepoint(coordinates)]
    print('selected item: ', selected_item )
    if(selected_item):
      if(selected_item[0] == item_to_match):
        print('this is the right answer!')
        return True
    return False

  def process_point_gain(self) -> None:
    """ Increments points and controls leveling up. """

    self.current_level.increment_score(points=1)

    if self.current_level.is_completed():
      if(self.completed_all_levels()):
        print('You have completed all levels!')
        self.quit()
      else:
        self.level_up()
    else:
      self.start_new_turn()

  def completed_all_levels(self):
    """ Returns True if all levels have been completed, False otherwise."""
    return self.current_level.level_number == len(self.levels)
  
  def level_up(self) -> None:
    """ Levels up the game."""
    print('level up')
    # level_number is 1 based, so just pass it in to get the right level from the list
    self.start_new_turn()
    self.current_level = self.levels[self.current_level.level_number]

  def start_new_turn(self) -> None:
    """ Resets screen and creates a new puzzle."""
    self.reset_sprites()
    self.render_new_puzzle()

  def reset_sprites(self) -> None:
    """ Remove all sprites."""
    SpriteHandler.kill_sprite(self.current_level.puzzle.item_to_match)
    SpriteHandler.kill_sprite_group(self.current_level.puzzle.items)

  def render_new_puzzle(self) -> None:
    """ Renders a new puzzle."""
    self.current_level.puzzle.generate()
    self.renderer.draw(self.current_level, self.status_bar)

  def quit(self):
    """ Quits game and exits program. """
    print('quitting game')
    pygame.quit()
    sys.exit()