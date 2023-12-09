import random

from funcs import load_pygame_image, quit_game
from models.item import Item
import pygame
from config.setup import game_items

pygame.init()

pygame.display.set_caption("Same Again")
frames_per_sec = pygame.time.Clock()
FPS = 30
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display_surface.fill((0, 0, 0))

# create item class for each item by pointing to image
items_group = pygame.sprite.Group()
# add first two items from game items to items sprite group using range
for i in range(4):
  item = Item(
      image=load_pygame_image('assets', 'images', game_items[i]['image']),
      text_identifier=game_items[i]['text_identifier'],
      word=game_items[i]['word']
    )
  items_group.add(item)

# PERHAPS MOVE TO SOME LEVEL MANAGER CLASS
def create_items_group():  
  x = 96
  y = SCREEN_HEIGHT - 300
  spacing = 60
  for item in items_group:
    item.update_rect(x, y)
    x += item.rect.width + spacing

create_items_group()

# randomly select and display one item from items using an algorithm
target_item: Item = random.choice(items_group.sprites())

# PERHAPS MOVE TO SOME LEVEL MANAGER CLASS
def reset_screen(group: pygame.sprite.Group, item: pygame.sprite.Sprite):
  for sprite in group:
    sprite.kill()
    group.remove(sprite)
  item.kill()

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit_game()
    
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        quit_game()
    
    display_surface.fill((0, 0, 0))
    display_surface.blit(target_item.image, ((SCREEN_WIDTH / 2) - target_item.rect.width / 2, 0))
    for item in items_group:
      display_surface.blit(item.image, (item.rect.x, item.rect.y))

    # on left click
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        selected_item = [s for s in items_group if s.rect.collidepoint(event.pos)]
        if(selected_item):
          if(selected_item[0] == target_item):
            print('this is the right answer!')
            reset_screen(items_group, target_item)
              
  pygame.display.update()
  frames_per_sec.tick(30)