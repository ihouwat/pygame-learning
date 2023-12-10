from abc import ABC
import random

from funcs import load_pygame_image, quit_game
from models.item import Item
import pygame
from config.setup import game_items
from pygame.sprite import Group

pygame.init()

# MOVE TO SOME SETUP FUNCTION
pygame.display.set_caption("Same Again")
frames_per_sec = pygame.time.Clock()
FPS = 30
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display_surface.fill((0, 0, 0))


# PERHAPS MOVE TO SOME RENDER CLASS
# create item class for each item by pointing to image
items: Group = pygame.sprite.Group()

def create_items_group() -> Group:
  used_indexes = set()
  while len(items) < 4:
    item_index = random.randint(0, len(game_items) - 1)
    if item_index not in used_indexes:
      used_indexes.add(item_index)
      sprite = Item(
          image=load_pygame_image('assets', 'images', game_items[item_index]['image']),
          text_identifier=game_items[item_index]['text_identifier'],
          word=game_items[item_index]['word']
        )
      items.add(sprite)
    else:
      continue

create_items_group()

# PERHAPS MOVE TO SOME RENDER CLASS
def position_items_group() -> None:  
  x = 96
  y = SCREEN_HEIGHT - 300
  spacing = 60
  for item in items:
    item.update_rect(x, y)
    x += item.rect.width + spacing

position_items_group()

target_item: Group = pygame.sprite.Group()
target_sprite: Item = None
# randomly select and display one item from items using an algorithm
def create_target_item() -> Group:
  global target_sprite
  target_sprite = random.choice(items.sprites())
  target_item.add(target_sprite)

create_target_item()

# PERHAPS MOVE TO SOME LEVEL MANAGER CLASS AND WE MIGHT NOT NEED THE GLOBALS AND AS MUCH LOGIC
# - Some class or method to generate puzzles (items and target item). Keep in mind that the puzzle might be different by level
# - Some class to manage renders (render sprites, update them, destroy them)
# - Some class to manage user input
# - Some class to manage levels and score

class LevelManager(ABC):
  def __init__(self, level_number: int, max_score: int):
    self.level = level_number
    self.max_score = max_score
  
  def __str__(self) -> str:
    return f'Level Manager for level {self.level}'
  
  def generate_puzzle(self, *groups: Group) -> None:
    ...

class Level1(LevelManager):
  def __init__(self, level_number: int, max_score: int):
    super().__init__(level_number, max_score)
  
  def generate_puzzle(self, *groups: Group) -> None:
    print('generating puzzle for level 1')
    create_items_group()
    position_items_group()
    create_target_item()
    
class Level2(LevelManager):
  def __init__(self, level_number: int, max_score: int):
    super().__init__(level_number, max_score)
  
  # IMPROVE THIS SEQUENCE OF FUNCTIONS IT IS REDUNDANT
  def generate_puzzle(self, *groups: Group) -> None:
    print('generating puzzle for level 2')
    create_items_group()
    position_items_group()
    create_target_item()
    
    
    # NEED TO MAKE THIS INTO A CONFIGURATION AND RENDER THE IMAGES AS GRAY WHEN WE FIRST CREATE THE SPRITES
    # OTHERWISE WE GET A KEYERROR WHEN WE TRY TO KILL THE SPRITES 
    self.turn_items_to_gray(*groups)
  
  def turn_items_to_gray(self, *groups: Group) -> None:
    for group in groups:
      for sprite in group:
        sprite.image = pygame.transform.grayscale(sprite.image)

class Game:
  def __init__(self):
    self.score: int = 0
    self.level: int = 1
    
    # extract this later
    self.levels: list[LevelManager] = [ Level1(level_number=1, max_score=1), Level2(level_number=2, max_score=5) ]
    self.level_manager: LevelManager = self.levels[self.level - 1]

  def process_point_gain(self, *groups: Group) -> None:
    """ Increments points, resets screen, and levels up if necessary """

    self.score = self.increment_score(self.score)
    print('score', self.score)

    # REDUNDANT CODE WITH RESETTING AND GENERATING PUZZLES.
    if self.score < self.level_manager.max_score:
      reset_sprite_groups(*groups)
      self.level_manager.generate_puzzle(*groups)
    else:
      reset_sprite_groups(*groups)
      self.level_up()
      self.level_manager.generate_puzzle(*groups)

  def increment_score(self, score: int) -> int:
    return score + 1
  
  def increment_level(self, level: int) -> int:
    return level + 1
  
  def level_up(self) -> None:
    print('level up')
    self.level = self.increment_level(self.level)
    self.score = 0
    self.level_manager = self.levels[self.level - 1]

# Create an instance of the Game class
game = Game()


# PERHAPS MOVE TO SOME LEVEL MANAGER CLASS
def reset_sprite_groups(*groups: Group):
  for group in groups:
    group.empty()

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit_game()
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        quit_game()
    
    display_surface.fill((0, 0, 0))
    for sprite in target_item:
      display_surface.blit(target_sprite.image, ((SCREEN_WIDTH / 2) - target_sprite.rect.width / 2, 0))
    for sprite in items:
      display_surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

    # on left click
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        selected_item = [s for s in items if s.rect.collidepoint(event.pos)]
        if(selected_item):
          if(selected_item[0] == target_sprite):
            print('this is the right answer!')
            game.process_point_gain(items, target_item)
              
  pygame.display.update()
  frames_per_sec.tick(30)