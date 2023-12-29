
import sys
from typing import Optional, Type

import pygame
from audio.audio_player import AudioPlayer
from config.logger import logger
from engine.animation_engine import AnimationEngine
from engine.animations import ScaleSprites
from engine.event_listener import EventListener
from engine.game_states import (
  GameCompletedState,
  LevelCompletedState,
  MenuOpenState,
  OpenMenuState,
  PausedState,
  PlayingState,
  StartNewTurnState,
  TransitionLevelState,
  TransitionTurnsState,
)
from engine.renderer import Renderer
from engine.sprite_handler import SpriteHandler
from game_objects.item_sprite import ItemSprite
from game_objects.level import Level
from models.game_state_machine import GameContext, GameStateMachine
from models.game_types import GameAction, GameState, Language, ProcessPointResult
from pygame.sprite import Group
from ui.game_menu import GameMenu
from ui.status_bar import StatusBar
from ui.ui_display import UIDisplay


class Game:
  """ Represents a game of Same Again.
  
  Attributes:
    renderer (Renderer): The renderer.
    ui_display (UIDisplay): The UI display.
    animation_engine (AnimationEngine): The animation engine.
    audio_player (AudioPlayer): The audio player.
    event_listener (EventListener): The event listener.
    status_bar (StatusBar): The status bar.
    game_menu (GameMenu): The game menu.
    levels (list[Level]): The list of levels.
    game_states (dict[GameState, Type[GameStateMachine]]): The game states.
    current_state (GameState): The current game state.
    current_level (Level): The current level.
    selected_language (Language): The selected language.
    player_name (str): The player name.
    item_to_match (ItemSprite): The item to match.
    items (Group): The group of items.
  """
  def __init__(self, renderer: Renderer, ui_display: UIDisplay, animation_engine: AnimationEngine, audio_player: AudioPlayer, event_listener: EventListener, status_bar: StatusBar, game_menu: GameMenu, levels: list[Level], language: Language):
    self.renderer: Renderer = renderer
    self.ui_display = ui_display
    self.animation_engine = animation_engine
    self.audio_player = audio_player
    self.event_listener: EventListener = event_listener
    self.status_bar: StatusBar = status_bar
    self.game_menu: GameMenu = game_menu
    self.levels: list[Level] = levels
    self.game_states: dict[GameState, Type[GameStateMachine]] = {
      GameState.PLAYING: PlayingState,
      GameState.MENU_IS_OPEN: MenuOpenState,
      GameState.LEVEL_COMPLETED: LevelCompletedState,
      GameState.GAME_COMPLETED: GameCompletedState,
      GameState.PAUSED: PausedState,
      GameState.TRANSITION_TO_NEXT_TURN: TransitionTurnsState,
      GameState.TRANSITION_TO_NEXT_LEVEL: TransitionLevelState,
      GameState.START_NEW_TURN: StartNewTurnState,
    }
    
    # also game state (candidates for extraction)
    self.current_state: GameState = GameState.MENU_IS_OPEN
    self.current_level: Level = self.levels[0]
    self.selected_language: Language = language
    self.player_name: str = "Player"
    self.item_to_match: ItemSprite = ItemSprite()
    self.items: Group = Group()

  def run(self, events: list[pygame.event.Event]) -> None:
    """ Primary method that runs the game.
    
    Args:
      events (list[pygame.event.Event]): The list of pygame events.
    """
    action: Optional[GameAction] = self.event_listener.process_events(events)
    self.items: Group = self.current_level.puzzle.items
    self.item_to_match: ItemSprite = self.current_level.puzzle.item_to_match
    
    if action == GameAction.QUIT:
      self.quit()
    
    game_context: GameContext = GameContext(game_instance=self, events=events, action=action, item_to_match=self.item_to_match, items=self.items)
    next_state: GameState = self.game_states[self.current_state](game_context).execute()
    self.renderer.draw(
      self.item_to_match,
      self.items,
      self.status_bar,
      self.ui_display,
      self.game_menu,
      self.current_state,
      self.current_level.level_number
      )
    self.current_state = next_state

  def reset_game_levels(self):
    """ Resets the game levels."""
    for level in self.levels:
      level.reset()
    self.current_level = self.levels[0]

  def save_user_settings(self, event: pygame.event.Event) -> None:
      """ Sets the language and player name from the game menu.
      
      Args:
        event (pygame.event.Event): The pygame event we extract the data from.
      """
      for lang in Language:
        if(lang.name == event.language):
          self.selected_language = lang
      if len(event.player) > 0:
        self.player_name = event.player
      
      self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)

  def match_detected(self, items: Group, item_to_match: ItemSprite, coordinates) -> bool:
    """ Returns True if a user has match an item correctly against a list of items, False otherwise.
    Args:
      items (Group): A group of items to match against.
      item_to_match (Sprite): The item to match.
      coordinates (tuple): The coordinates of the mouse click event.
    """
    selected_item: list[ItemSprite] = [sprite for sprite in items if sprite.rect.collidepoint(coordinates)]
    if(selected_item):
      if(selected_item[0].metadata == item_to_match.metadata):
        logger.info('this is the right answer!')
        return True
    return False

  def process_point_gain(self) -> ProcessPointResult:
    """ Increments points and controls leveling up. """

    self.current_level.increment_score(points=1)

    if self.current_level.is_completed():
      return ProcessPointResult.LEVEL_COMPLETED

    else:
      return ProcessPointResult.START_NEW_TURN

  def completed_all_levels(self):
    """ Returns True if all levels have been completed, False otherwise."""
    return self.current_level.level_number == len(self.levels)
  
  def level_up(self) -> None:
    """ Levels up the game."""
    logger.info('level up')
    # level_number is 1 based, so just pass it in to get the right level from the list
    self.current_level = self.levels[self.current_level.level_number]
    # play hand clap sound effect
    # self.audio_player.playsound(sound='audio/level_up.wav', vol=0.5)
    self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)


  def start_new_turn(self) -> None:
    """ Generates sprites t0 create a new puzzle"""
    item_to_match, items = self.current_level.puzzle.generate()
    self.spawn_sprites(items, item_to_match)
  
  def spawn_sprites(self, items: Group, item_to_match: ItemSprite) -> None:
    """ Scales sprites out and in to create a spawn effect.
    
    Args:
      items (Group): The group of sprites.
      item_to_match (ItemSprite): The item to match.
    """
    if(item_to_match.scale != 0):
      pygame.time.wait(350)
      # scale sprites down to prepare for spawn in, and then spawn in
      self.animation_engine.add_animation(ScaleSprites(scaling_factor=-100, items=items, item_to_match=item_to_match)
      ).execute()
    else:
      self.animation_engine.add_animation(ScaleSprites(scaling_factor=10, items=items, item_to_match=item_to_match)
    ).execute()

  def transition_to_next_turn(self, items: Group, item_to_match: ItemSprite):
    """ Scales sprites down, kills sprites, and updates UI.
    
    Args:
      items (Group): The group of sprites.
      item_to_match (ItemSprite): The item to match.
    """
    # play some sound effect to indicate success
    # self.audio_player.playsound(sound='audio/incorrect.wav', vol=0.5)
    # play the word for the item that was matched
    # self.audio_player.playsound(sound='audio/correct.wav', vol=0.5)

    self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)
    pygame.time.wait(150)
    self.animation_engine.add_animation(
      ScaleSprites(scaling_factor=-10, items=items, item_to_match=item_to_match)
    ).execute()
    self.kill_sprites()

  def kill_sprites(self) -> None:
    """ Remove all sprites."""
    if(self.current_level.puzzle.item_to_match):
      SpriteHandler.kill_sprite(self.current_level.puzzle.item_to_match)
    if(self.current_level.puzzle.items):
      SpriteHandler.kill_sprite_group(self.current_level.puzzle.items)

  def quit(self) -> None:
    """ Quits game and exits program. """
    logger.info('quitting game')
    pygame.quit()
    sys.exit()