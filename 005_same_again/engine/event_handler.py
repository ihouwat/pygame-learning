import pygame
from config.settings import START_GAME
from models.game_types import GameAction


class EventListener():
  """ Handles events in the game. """
  
  def process_events(self, events: list[pygame.event.Event]) -> GameAction | None:
    """ Primary method that listens to and processes a list of events and returns a game action.
    
    Args:
      events (list[pygame.event.Event]): A list of pygame events.
    """
    for event in events:
      if event.type == pygame.QUIT:
        return GameAction.QUIT
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          return GameAction.QUIT

      # on left click
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          return GameAction.OBJECT_SELECTED
      
      if event.type == START_GAME:
        return GameAction.START_GAME