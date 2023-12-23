import pygame
from config.prepare_game import frames_per_sec, game
from config.settings import FPS


def run_loop():
  while 1:
    game.run(events=pygame.event.get())
    pygame.display.update()
    frames_per_sec.tick(FPS)

if __name__ == "__main__":
  run_loop()