
import pygame
from config.prepare import frames_per_sec, game
from config.settings import FPS

while 1:
  game.run(events=pygame.event.get())
  pygame.display.update()
  frames_per_sec.tick(FPS)