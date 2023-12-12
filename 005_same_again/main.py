from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import random
from typing import Tuple

from funcs import load_pygame_image
from models.item import Item
import pygame
from config.setup import game_items
from pygame.sprite import Group, Sprite
import sys

pygame.init()

# MOVE TO SOME SETUP FUNCTION
frames_per_sec = pygame.time.Clock()
FPS = 30
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# PERHAPS MOVE TO SOME LEVEL MANAGER CLASS AND WE MIGHT NOT NEED THE GLOBALS AND AS MUCH LOGIC
# - DPME Some class or method to generate puzzles (items and target item). Keep in mind that the puzzle might be different by level
# - Some class to manage user input
# - DONE - Renderer ClassSome class to manage renders (render sprites, update them, destroy them)
# - DONE - Game class: Some class to manage levels and score
# - DONE Change Level to Puzzle and then a Level takes in a puzzle, max score, and level number

class Option(Enum):
  GRAYSCALE = 'grayscale'

class SpriteHandler:

  @staticmethod
  def create_items_group(list_of_items: list, max_number: int, option: Option = None) -> Group:
    items = SpriteHandler.pick_items_from_list(list_of_items, max_number)
    
    group = pygame.sprite.Group()
    for item in items:
      src_image = load_pygame_image('assets', 'images', item['image'])

      if option == Option.GRAYSCALE:
        src_image=pygame.transform.grayscale(src_image)

      group.add(Item(
        image=src_image,
        text_identifier=item['text_identifier'],
        word=item['word']
      ))
    return group
  
  @staticmethod
  def pick_items_from_list(list_of_items: list, max_number: int):
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
    return random.choice(items.sprites())
  
  @staticmethod
  def reset_sprite_group(group: Group):
    for sprite in group:
      sprite.kill()

class Renderer:
  def __init__(self):
    self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Same Again")

  def update_screen(self, items: Group, matched_item: Sprite) -> None:
    self.arrange_items(items)
    self.render_screen(items, matched_item)

  def arrange_items(self, items: Group) -> None:  
    total_items_width = sum(item.rect.width for item in items)
    # subtract total items width from screen width and divide by number of items + 1 to distribute spacing evenly between items
    spacing = (SCREEN_WIDTH - total_items_width) / (len(items) + 1)
    x = spacing
    y = SCREEN_HEIGHT - 300

    for item in items:
      item.update_rect(x, y)
      x += item.rect.width + spacing

  def render_screen(self, items: Group, matched_item: Sprite) -> None:
    self.display_surface.fill((0, 0, 0))
    self.display_surface.blit(matched_item.image, ((SCREEN_WIDTH / 2) - matched_item.rect.width / 2, 0))
    for sprite in items:
      self.display_surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

@dataclass
class Puzzle(ABC):

  @property
  @abstractmethod
  def description(self) -> str:
    pass

  def generate(self) -> Tuple[Sprite, Group]:
    ...

class ItemPuzzle(Puzzle):
  
  @property
  def description(self) -> str:
    return'Match a colored image to another image in a list of images'
  
  # REFACTOR: THIS FUNCTION IS REDUNDANT
  def generate(self):
    print('generating item puzzle')
    new_group = SpriteHandler.create_items_group(list_of_items=game_items, max_number=4)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    return item_to_match, new_group
    
class GrayscaleItemPuzzle(Puzzle):
  
  @property
  def description(self) -> str:
    return 'Match a grayscale image to another image in a list of grayscale images'
  
  def generate(self):
    print('generating grayscale item puzzle')
    new_group = SpriteHandler.create_items_group(list_of_items=game_items, max_number=4, option=Option.GRAYSCALE)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    return item_to_match, new_group

class SpokenWordPuzzle(Puzzle):
  pass

class ShapesPuzzle(Puzzle):
  pass

@dataclass
class Level:
  puzzle: int
  max_score: int
  level_number: int
  score: int = 0
  
  def increment_score(self, points: int) -> int:
    self.score = self.score + points
    print(f'new score for {self.level_number}: {self.score}')
    return self.score

class Game:
  def __init__(self, renderer: Renderer, levels: list[Puzzle]):
    self.levels: list[Puzzle] = levels
    self.current_level: Level = self.levels[0]
    self.items: Group = pygame.sprite.Group()
    self.matched_item: Item = None
    self.renderer: Renderer = renderer
  
    self.create_puzzle()

  # ADD TO EVENT HANDLING CLASS OR RENDERER CLASS????
  def check_match(self, items: Group, matched_item: Sprite, coordinates) -> bool:
    selected_item = [sprite for sprite in items if sprite.rect.collidepoint(coordinates)]
    print('selected item: ', selected_item )
    if(selected_item):
      if(selected_item[0] == matched_item):
        print('this is the right answer!')
        return True
    return False

  def process_point_gain(self) -> None:
    """ Increments points and levels up if the max score is reached. """

    new_score = self.current_level.increment_score(1)

    if new_score < self.current_level.max_score:
      self.create_puzzle()
    else:
      self.level_up()
  
  def level_up(self) -> None:
    print('level up')
    self.current_level = self.levels[self.current_level.level_number] # level_number is 1 based, so just pass it in to get the right level from the list
    self.create_puzzle()
  
  def create_puzzle(self) -> None:
    SpriteHandler.reset_sprite_group(self.items)
    self.matched_item, self.items = self.current_level.puzzle.generate()
    self.renderer.update_screen(self.items, self.matched_item)
  
  def quit():
    """
    Quits game and exits program.
    """
    pygame.quit()
    sys.exit()

# MOVE TO SOME SETUP FUNCTION
levels = [ 
          Level(puzzle=ItemPuzzle(), level_number=1, max_score=5),
          Level(puzzle=GrayscaleItemPuzzle(), level_number=2, max_score=5)
        ]
renderer = Renderer()
game = Game(renderer=renderer, levels=levels)

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      game.quit()
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        game.quit()

    # on left click
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        if(game.check_match(game.items, game.matched_item, event.pos)):
          game.process_point_gain()
              
  pygame.display.update()
  frames_per_sec.tick(30)