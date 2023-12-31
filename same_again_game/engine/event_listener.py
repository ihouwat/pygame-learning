from typing import Optional

import pygame
from config.settings import (
  ENTERED_WRONG_ANSWER,
  MATCH_DETECTED,
  RESUME_GAME,
  START_GAME,
)
from models.game_types import GameAction


class EventListener():
  """ Handles events in the game. """
  
  def process_events(self, events: list[pygame.event.Event]) -> Optional[GameAction]:
    """ Primary method that listens to and processes a list of events and returns a game action.
    
    Args:
      events (list[pygame.event.Event]): A list of pygame events.
    """
    for event in events:
      
      if (event.type == pygame.ACTIVEEVENT):
        if (event.gain == 1):
          return GameAction.MOUSE_ENTERED_WINDOW
        else:
          return GameAction.MOUSE_EXITED_WINDOW

      if event.type == pygame.QUIT:
        return GameAction.QUIT
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          return GameAction.OPEN_MENU

      # on left click
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          return GameAction.ITEM_SELECTED
            
      if event.type == MATCH_DETECTED:
        return GameAction.MATCH_DETECTED
      
      if event.type == ENTERED_WRONG_ANSWER:
        return GameAction.WRONG_ITEM_SELECTED

      if event.type == START_GAME:
        return GameAction.START_NEW_GAME
      
      if event.type == RESUME_GAME:
        return GameAction.RESUME_GAME