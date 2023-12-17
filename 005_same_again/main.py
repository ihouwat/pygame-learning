
import pygame
from config.game_setup import puzzles
from engine.event_handler import EventHandler
from engine.renderer import Renderer
from game_manager import GameManager
from game_objects.models.level import Level
from config.settings import FPS

pygame.init()

# MOVE TO GAME SETUP FUNCTION
frames_per_sec = pygame.time.Clock()
levels = [ Level(puzzle=puzzle, level_number=i+1, max_score=4) for i, puzzle in enumerate(puzzles) ]
game = GameManager(renderer=Renderer(), levels=levels)
event_handler = EventHandler(game=game)

while 1:
  event_handler.handle(events=pygame.event.get())  
  pygame.display.update()
  frames_per_sec.tick(FPS)