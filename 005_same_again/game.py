
import sys

import pygame
from engine.event_handler import EventListener
from engine.renderer import Renderer
from engine.sprite_handler import SpriteHandler
from game_objects.entities.level import Level
from game_objects.entities.puzzles import Puzzle
from models.types import GameAction, Language
from pygame.sprite import Group, Sprite
from ui.game_menu import GameMenu
from ui.status_bar import StatusBar


class Game:
  """ Represents a game of Same Again."""

  def __init__(self, renderer: Renderer, event_listener: EventListener, status_bar: StatusBar, game_menu: GameMenu, levels: list[Puzzle], language: str):
    self.renderer: Renderer = renderer
    self.event_listener: EventListener = event_listener
    self.status_bar: StatusBar = status_bar
    self.game_menu: GameMenu = game_menu
    self.levels: list[Puzzle] = levels
    
    self.current_level: Level = self.levels[0]
    self.selected_language: Language = None
    self.player_name: str = "Player"

    self.renderer.draw_game_menu(self.game_menu)


  def run(self, events: list[pygame.event.Event]) -> None:
    """ Primary method that runs the game."""
    action = self.event_listener.process_events(events)
    items = self.current_level.puzzle.items
    item_to_match = self.current_level.puzzle.item_to_match

    if action == GameAction.START_GAME:
      self.set_language_and_name(events)          
      self.start_new_turn()    
    if action == GameAction.QUIT:
      self.quit()
    if action == GameAction.OBJECT_SELECTED and items and item_to_match:
      if(self.match_detected(items, item_to_match, pygame.mouse.get_pos())):
        self.process_point_gain()

  def set_language_and_name(self, events: list[pygame.event.Event]) -> None:
      for lang in Language:
        if(lang.name == events[0].language):
          self.selected_language = lang
      if len(events[0].player) > 0:
        self.player_name = events[0].player

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
    self.current_level = self.levels[self.current_level.level_number]
    self.start_new_turn()

  def start_new_turn(self) -> None:
    """ Resets screen and creates a new puzzle."""
    self.reset_sprites()
    self.current_level.puzzle.generate()
    self.renderer.draw(level=self.current_level, status_bar=self.status_bar, player_name=self.player_name, language=self.selected_language)

  def reset_sprites(self) -> None:
    """ Remove all sprites."""
    if(self.current_level.puzzle.item_to_match):
      SpriteHandler.kill_sprite(self.current_level.puzzle.item_to_match)
    if(self.current_level.puzzle.items):
      SpriteHandler.kill_sprite_group(self.current_level.puzzle.items)

  def quit(self):
    """ Quits game and exits program. """
    print('quitting game')
    pygame.quit()
    sys.exit()