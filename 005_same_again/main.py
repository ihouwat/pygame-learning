from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import random
from typing import Tuple

from funcs import load_pygame_image
from models.item import Item
import pygame
from config.setup import GameItemConfig, GAMEOBJECTTYPE, game_items
from pygame.sprite import Group, Sprite
import sys

pygame.init()

# MOVE TO SOME SETUP FUNCTION
frames_per_sec = pygame.time.Clock()
FPS = 30
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

class Option(Enum):
  """ Represents an option to be applied to a sprite."""
  GRAYSCALE = 'grayscale'
  SHAPES = 'shapes'

class SpriteHandler:
  """ Handles the creation of sprites and sprite groups. """
  
  game_items: list[GameItemConfig] = game_items
  
  @staticmethod
  def create_sprite_group(max_number: int, option: Option = None) -> Group:
    """ Creates a sprite group given a list of items."""
    
    if option == Option.SHAPES:
      filtered_list = game_items[GAMEOBJECTTYPE.SHAPE]
    else:
      filtered_list = game_items[GAMEOBJECTTYPE.ITEM]
    items: list = SpriteHandler.pick_items_from_list(filtered_list, max_number)
    group: Group = SpriteHandler.create_group(items, option)
    return group

  @staticmethod
  def create_group(items: list[GameItemConfig], option: Option) -> Group:
    """ Creates a sprite group out of a list of items.
    
    Args:
      items (list): A list of items to be converted to sprites.
      option (Option): An option to be applied to the sprite.
    """
    group = pygame.sprite.Group()
    for item in items:
      if option == Option.SHAPES:
        src_image = item.image
      else:
        src_image = load_pygame_image('assets', 'images', item.image)

      if option == Option.GRAYSCALE:
        src_image=pygame.transform.grayscale(src_image)

      group.add(Item(
      image=src_image,
      text_identifier=item.text_identifier,
      word=item.word
    ))

    return group
  
  @staticmethod
  def pick_items_from_list(list_of_items: list[GameItemConfig], max_number: int) -> list:
    """ Picks a random number of items from a list of items. 
    
    Args:
      list_of_items (list): A list of items to pick from.
      max_number (int): The maximum number of items to pick.
    """
    used_indexes = set()
    items = []

    while len(items) < max_number:
      item_index = random.randint(0, len(list_of_items) - 1)
      if item_index not in used_indexes:
        used_indexes.add(item_index)
        items.append(list_of_items[item_index])
      else:
        continue
    return items

  @staticmethod
  def pick_item_to_match(items: Group) -> Sprite:
    """ Picks a random item from a sprite group."""
    return random.choice(items.sprites())
  
  @staticmethod
  def reset_sprite_group(group: Group) -> None:
    """ Removes all sprites from a sprite group."""
    for sprite in group:
      sprite.kill()

class Renderer:
  """ Handles the rendering of the game."""
  def __init__(self):
    self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Same Again")

  def update_screen(self, items: Group, target_match: Sprite) -> None:
    """ Updates the screen with a new set of items and a target item."""
    self.arrange_items(items)
    self.render_screen(items, target_match)

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

  def render_screen(self, items: Group, item_to_match: Sprite) -> None:
    """ Renders the screen with a new set of items and a target item."""
    self.display_surface.fill((0, 0, 0))
    self.display_surface.blit(item_to_match.image, ((SCREEN_WIDTH / 2) - (item_to_match.rect.width / 2), 100))
    for sprite in items:
      self.display_surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

@dataclass(frozen=True, kw_only=True)
class Puzzle(ABC):
  """ 
    Represents a puzzle that can be played in the game.
    
    Attributes:
    description(str): A description of the puzzle.
    option(Option): An option to be applied to the puzzle.
    max_number_of_items(int): The maximum number of items to be used in the puzzle.
    """

  @property
  @abstractmethod
  def description(self) -> str:
    pass
  
  @property
  @abstractmethod
  def option(self) -> Option:
    pass
  
  @property
  @abstractmethod
  def max_number_of_items(self) -> int:
    pass

  def generate(self) -> Tuple[Sprite, Group]:
    """ Generates a new puzzle."""
    new_group = SpriteHandler.create_sprite_group(max_number=self.max_number_of_items, option=self.option)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    return item_to_match, new_group

class ItemPuzzle(Puzzle):
  """ Puzzle implementation for matching colored images."""

  @property
  def description(self) -> str:
    return'Match a colored image to another image in a list of images'
  
  @property
  def option(self) -> Option:
    return None
  
  @property
  def max_number_of_items(self) -> int:
    return 4

class GrayscaleItemPuzzle(Puzzle):
  """ Puzzle implementation for matching grayscale images."""

  @property
  def description(self) -> str:
    return 'Match a grayscale image to another image in a list of grayscale images'
  
  @property
  def option(self) -> Option:
    return Option.GRAYSCALE
  
  @property
  def max_number_of_items(self) -> int:
    return 4

class SpokenWordPuzzle(Puzzle):
  """ Puzzle implementation for matching spoken words."""
  pass

class ShapesPuzzle(Puzzle):
  """ Puzzle implementation for matching basic shapes."""

  @property
  def description(self) -> str:
    return 'Match a shape to another shape in a list of shapes'
  
  @property
  def option(self) -> Option:
    return Option.SHAPES
  
  @property
  def max_number_of_items(self) -> int:
    return 4

@dataclass (kw_only=True)
class Level:
  """ Represents a level in the game.

  Attributes:
    puzzle (Puzzle): The puzzle to be played in the level.
    max_score (int): The maximum score that can be achieved in the level.
    level_number (int): The level number.
    score (int): The current score.
  """

  puzzle: Puzzle
  max_score: int
  level_number: int
  score: int = 0
  
  def increment_score(self, points: int) -> int:
    """ Increments the score by a given number of points."""
    self.score = self.score + points
    print(f'new score for level {self.level_number}: {self.score}')
    return self.score

  def is_completed(self) -> bool:
    """ Returns True if the level is completed, False otherwise."""
    return self.score == self.max_score

class Game:
  """ Represents a game of Same Again."""

  def __init__(self, renderer: Renderer, levels: list[Puzzle]):
    self.levels: list[Puzzle] = levels
    self.current_level: Level = self.levels[0]
    self.items: Group = pygame.sprite.Group()
    self.item_to_match: Item = None
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
    SpriteHandler.reset_sprite_group(self.items)
    self.item_to_match, self.items = self.current_level.puzzle.generate()
    self.renderer.update_screen(self.items, self.item_to_match)
  
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

  def __init__(self, game: Game):
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

# MOVE TO SOME SETUP FUNCTION
levels = [ 
          Level(puzzle=ShapesPuzzle(), level_number=1, max_score=5),
          Level(puzzle=GrayscaleItemPuzzle(), level_number=2, max_score=5)
        ]
game = Game(renderer=Renderer(), levels=levels)
event_handler = EventHandler(game=game)

while 1:
  event_handler.handle(events=pygame.event.get())  
  pygame.display.update()
  frames_per_sec.tick(30)