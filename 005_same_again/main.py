import sys

import pygame
from config.game_setup import puzzles
from game_objects.models.item import Item
from game_objects.models.puzzle import Puzzle
from engine.sprite_handler import SpriteHandler
from engine.renderer import Renderer
from pygame.sprite import Group, Sprite
from game_objects.models.level import Level

pygame.init()

# MOVE TO SOME SETUP FUNCTION
frames_per_sec = pygame.time.Clock()
FPS = 30



class GameManager:
  """ Represents a game of Same Again."""

  def __init__(self, renderer: Renderer, levels: list[Puzzle]):
    self.levels: list[Puzzle] = levels
    self.current_level: Level = self.levels[0]
    self.items: Group = pygame.sprite.Group()
    self.item_to_match: Item = pygame.sprite.Sprite()
    self.renderer: Renderer = renderer
  
    self.create_puzzle()

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
      self.create_puzzle()

  def completed_all_levels(self):
    """ Returns True if all levels have been completed, False otherwise."""
    return self.current_level.level_number == len(self.levels)
  
  def level_up(self) -> None:
    """ Levels up the game."""
    print('level up')
    # level_number is 1 based, so just pass it in to get the right level from the list
    self.current_level = self.levels[self.current_level.level_number]
    self.create_puzzle()
  
  def create_puzzle(self) -> None:
    """ Creates a new puzzle and resets screen."""
    self.reset_sprites()
    self.item_to_match, self.items = self.current_level.puzzle.generate()
    self.renderer.update_screen(self.items, self.item_to_match)
    
  def reset_sprites(self) -> None:
    """ Remove all sprites."""
    SpriteHandler.kill_sprite(self.item_to_match)
    SpriteHandler.kill_sprite_group(self.items)
  
  def quit(self):
    """ Quits game and exits program. """
    print('quitting game')
    pygame.quit()
    sys.exit()

class EventHandler():
  """ Handles events in the game.
  
  Attributes:
    game (Game): The game to handle events for.
  """

  def __init__(self, game: GameManager):
    self.game = game
  
  def handle(self, events: list[pygame.event.Event]):
    """ Primary method that handles a list of events."""
    for event in events:
      if event.type == pygame.QUIT:
        game.quit()
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          game.quit()

      # on left click
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          if(game.match_detected(game.items, game.item_to_match, event.pos)):
            game.process_point_gain()


levels = [ Level(puzzle=puzzle, level_number=i+1, max_score=4) for i, puzzle in enumerate(puzzles) ]
game = GameManager(renderer=Renderer(), levels=levels)
event_handler = EventHandler(game=game)

while 1:
  event_handler.handle(events=pygame.event.get())  
  pygame.display.update()
  frames_per_sec.tick(30)