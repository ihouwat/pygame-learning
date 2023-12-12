from abc import ABC
import random

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
# - Some class or method to generate puzzles (items and target item). Keep in mind that the puzzle might be different by level
# - Some class to manage user input
# - DONE - Renderer ClassSome class to manage renders (render sprites, update them, destroy them)
# - DONE - Game class: Some class to manage levels and score
# - Change Level to Puzzle and then a Level takes in a puzzle, max score, and level number

class SpriteHandler:

  @staticmethod
  def create_items_group(list_of_items: list, max_number: int) -> Group:
    used_indexes = set()
    items = pygame.sprite.Group()

    while len(items) < max_number:
      item_index = random.randint(0, len(list_of_items) - 1)
      if item_index not in used_indexes:
        used_indexes.add(item_index)
        sprite = Item(
            image=load_pygame_image('assets', 'images', list_of_items[item_index]['image']),
            text_identifier=list_of_items[item_index]['text_identifier'],
            word=list_of_items[item_index]['word']
          )
        items.add(sprite)
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

# SHOULD BECOME A PUZZLE CLASS AND NOT HAVE TO WORRY ABOUT LEVELS OR SCORE
class Puzzle(ABC):
  def __init__(self, level: int, max_score: int):
    self.level: int = level
    self.max_score: int = max_score
    self.description: str = None
  
  def __str__(self) -> str:
    return f'Level Manager for level {self.level}'
  
  def generate_puzzle(self) -> None:
    ...

class ItemPuzzle(Puzzle):
  def __init__(self, level: int, max_score: int):
    super().__init__(level, max_score)
    self.description = 'Match a colored image to another image in a list of images'
  
  # REFACTOR: THIS FUNCTION IS REDUNDANT
  def generate_puzzle(self) -> None:
    print('generating puzzle for level 1')
    new_group = SpriteHandler.create_items_group(list_of_items=game_items, max_number=4)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    return item_to_match, new_group
    
class GrayscaleItemPuzzle(Puzzle):
  def __init__(self, level: int, max_score: int):
    super().__init__(level, max_score)
    self.description = 'Match a grayscale image to another image in a list of grayscale images'
  
  def generate_puzzle(self) -> None:
    print('generating puzzle for level 2')
    new_group = SpriteHandler.create_items_group(list_of_items=game_items, max_number=4)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    
    # NEED TO MAKE THIS INTO A CONFIGURATION AND RENDER THE IMAGES AS GRAY WHEN WE FIRST CREATE THE SPRITES
    # OTHERWISE WE GET A KEYERROR WHEN WE TRY TO KILL THE SPRITES 
    self.turn_items_to_gray(new_group)
    return item_to_match, new_group

  def turn_items_to_gray(self, group: Group) -> None:
    for sprite in group:
      sprite.image = pygame.transform.grayscale(sprite.image)

class SpokenWordPuzzle(Puzzle):
  pass

class ShapesPuzzle(Puzzle):
  pass

class Game:
  def __init__(self, renderer: Renderer, levels: list[Puzzle]):
    self.score: int = 0
    self.level_number: int = 1
    self.levels: list[Puzzle] = levels
    self.current_level: Puzzle = self.levels[self.level_number - 1]
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

    self.score = self.increment_score(self.score)
    print('updated score: ', self.score)

    if self.score < self.current_level.max_score:
      self.create_puzzle()
    else:
      self.level_up()

  def increment_score(self, score: int) -> int:
    return score + 1
  
  def level_up(self) -> None:
    print('level up')
    self.level_number += 1
    self.score = 0
    self.current_level = self.levels[self.level_number - 1]
    self.create_puzzle()
  
  def create_puzzle(self) -> None:
    SpriteHandler.reset_sprite_group(self.items)
    self.matched_item, self.items = self.current_level.generate_puzzle()
    self.renderer.update_screen(self.items, self.matched_item)
  
  def quit():
    """
    Quits game and exits program.
    """
    pygame.quit()
    sys.exit()

# MOVE TO SOME SETUP FUNCTION
# TURN INTO A CONFIGURATION TUPLE OR LEVEL willCLASS (PUZZLE, MAX_SCORE, LEVEL_NUMBER)
levels = [ 
          ItemPuzzle(level=1, max_score=5),
          GrayscaleItemPuzzle(level=2, max_score=5)
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