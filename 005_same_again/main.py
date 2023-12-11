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
# - Some class to manage renders (render sprites, update them, destroy them)
# - Some class to manage user input
# - Some class to manage levels and score

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

  def position_items_group(self, items: Group) -> None:  
    x = 96
    y = SCREEN_HEIGHT - 300
    spacing = 60
    for item in items:
      item.update_rect(x, y)
      x += item.rect.width + spacing

  def render_screen(self, items: Group, matched_item: Sprite) -> None:
    self.display_surface.fill((0, 0, 0))
    self.display_surface.blit(matched_item.image, ((SCREEN_WIDTH / 2) - matched_item.rect.width / 2, 0))
    for sprite in items:
      self.display_surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

class Level(ABC):
  def __init__(self, level: int, max_score: int):
    self.level: int = level
    self.max_score: int = max_score
    self.description: str = None
  
  def __str__(self) -> str:
    return f'Level Manager for level {self.level}'
  
  def generate_puzzle(self, items_group: Group) -> None:
    ...

class ItemLevel(Level):
  def __init__(self, level: int, max_score: int):
    super().__init__(level, max_score)
    self.description = 'Match a colored image to another image in a list of images'
  
  # REFACTOR: THIS FUNCTION IS REDUNDANT, AND IT IS BOTH RESETTING AND GENERATING SPRITES.
  def generate_puzzle(self, items_group: Group) -> None:
    print('generating puzzle for level 1')
    SpriteHandler.reset_sprite_group(items_group)
    new_group = SpriteHandler.create_items_group(list_of_items=game_items, max_number=4)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    return item_to_match, new_group
    
class GrayscaleItemLevel(Level):
  def __init__(self, level: int, max_score: int):
    super().__init__(level, max_score)
    self.description = 'Match a grayscale image to another image in a list of grayscale images'
  
  def generate_puzzle(self, items_group: Group) -> None:
    print('generating puzzle for level 2')
    SpriteHandler.reset_sprite_group(items_group)
    new_group = SpriteHandler.create_items_group(list_of_items=game_items, max_number=4)
    item_to_match = SpriteHandler.pick_item_to_match(new_group)
    
    # NEED TO MAKE THIS INTO A CONFIGURATION AND RENDER THE IMAGES AS GRAY WHEN WE FIRST CREATE THE SPRITES
    # OTHERWISE WE GET A KEYERROR WHEN WE TRY TO KILL THE SPRITES 
    self.turn_items_to_gray(new_group)
    return item_to_match, new_group

  def turn_items_to_gray(self, group: Group) -> None:
    for sprite in group:
      sprite.image = pygame.transform.grayscale(sprite.image)

class SpokenWordLevel(Level):
  pass

class ShapesLevel(Level):
  pass

class Game:
  def __init__(self, renderer: Renderer, levels: list[Level]):
    self.score: int = 0
    self.level_number: int = 1
    self.levels: list[Level] = levels
    self.current_level: Level = self.levels[self.level_number - 1]
    self.items: Group = pygame.sprite.Group()
    self.matched_item: Item = None
    self.renderer: Renderer = renderer

  def start(self) -> None:
    self.create_puzzle()

  # ADD TO EVENT HANDLING CLASS????
  def check_match(self, items: Group, matched_item: Sprite, coordinates) -> bool:
    selected_item = [sprite for sprite in items if sprite.rect.collidepoint(coordinates)]
    print('selected item: ', selected_item )
    if(selected_item):
      if(selected_item[0] == matched_item):
        print('this is the right answer!')
        return True
    return False

  def process_point_gain(self) -> None:
    """ Increments points, resets screen, and levels up if necessary """

    self.score = self.increment_score(self.score)
    print('updated score: ', self.score)

    # REDUNDANT CODE WITH RESETTING AND GENERATING PUZZLES.
    if self.score < self.current_level.max_score:
      self.create_puzzle()
    else:
      self.level_up()
      self.create_puzzle()

  def increment_score(self, score: int) -> int:
    return score + 1
  
  def level_up(self) -> None:
    print('level up')
    self.level_number += 1
    self.score = 0
    self.current_level = self.levels[self.level_number - 1]
  
  def create_puzzle(self) -> None:
    self.matched_item, self.items = self.current_level.generate_puzzle(self.items)
    self.renderer.position_items_group(self.items)
    self.renderer.render_screen(self.items, self.matched_item)
  
  def quit():
    """
    Quits game and exits program.
    """
    pygame.quit()
    sys.exit()

# MOVE TO SOME SETUP FUNCTION
levels = [ 
          ItemLevel(level=1, max_score=5),
          GrayscaleItemLevel(level=2, max_score=5)
        ]
renderer = Renderer()
game = Game(renderer=renderer, levels=levels)
game.start()

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