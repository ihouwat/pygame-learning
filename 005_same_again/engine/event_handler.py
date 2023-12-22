import sys

import pygame
from game import Game


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
        self.quit()
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.quit()

      # on left click
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          if(self.game.match_detected(self.game.items, self.game.item_to_match, event.pos)):
            self.game.process_point_gain()
  
  def quit(self):
    """ Quits game and exits program. """
    print('quitting game')
    pygame.quit()
    sys.exit()

