
import pygame
from config.prepare import puzzles
from config.settings import FPS
from engine.event_handler import EventListener
from engine.renderer import Renderer
from game import Game
from game_objects.entities.level import Level

pygame.init()

# MOVE TO GAME SETUP FUNCTION
frames_per_sec = pygame.time.Clock()
levels = [ Level(puzzle=puzzle, level_number=i+1, max_score=4) for i, puzzle in enumerate(puzzles) ]
game = Game(renderer=Renderer(), levels=levels, event_listener=EventListener())

while 1:
  game.run(events=pygame.event.get())  
  pygame.display.update()
  frames_per_sec.tick(FPS)