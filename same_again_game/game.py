
import sys
from typing import Optional, Type

import pygame
from audio.audio_player import AudioPlayer
from config.logger import logger
from config.settings import (
  ANIMATION_DELAY,
  FONT_LARGE,
  FONT_NAME,
  SCREEN_HEIGHT,
  SCREEN_WIDTH,
)
from engine.animation_engine import AnimationEngine
from engine.animations import ScaleSprite, TextTransition
from engine.event_listener import EventListener
from engine.game_states import (
  EndTurnState,
  GameCompletedState,
  LevelCompletedState,
  MenuOpenState,
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
from game_objects.text_element import TextElement
from models.game_state_machine import GameContext, GameStateMachine
from models.game_types import (
  Color,
  GameAction,
  GameState,
  Language,
  ProcessPointResult,
  Soundtracks,
  SoundType,
  TextElementType,
)
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
    text_elements (list[TextElement]): The list of text elements.
  """
  def __init__(self, renderer: Renderer, ui_display: UIDisplay, animation_engine: AnimationEngine, audio_player: AudioPlayer, event_listener: EventListener, status_bar: StatusBar, game_menu: GameMenu, levels: list[Level], language: Language, soundtrack: Soundtracks):
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
      GameState.END_TURN: EndTurnState
    }
    
    # also game state (candidates for extraction)
    self.current_state: GameState = GameState.MENU_IS_OPEN
    self.current_level: Level = self.levels[0]
    self.selected_language: Language = language
    self.player_name: str = "Player"
    self.item_to_match: ItemSprite = ItemSprite()
    self.items: Group = Group()
    self.text_elements: dict[TextElementType, TextElement] = {
      TextElementType.LEVEL_UP: TextElement(
                    text=f'Level {self.current_level.level_number}',
                    font=pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_LARGE),
                    color=pygame.Color(Color.WHITE.value),
                    x=-450,
                    y=(SCREEN_HEIGHT // 2) - FONT_LARGE,
                    ),
      TextElementType.GAME_COMPLETED: TextElement(
                    text='YOU WIN!',
                    font=pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_LARGE),
                    color=pygame.Color(Color.WHITE.value),
                    x=-600,
                    y=(SCREEN_HEIGHT // 2) - FONT_LARGE,
                    ),
    }
    self.soundtrack: Soundtracks = soundtrack
    
    # start music
    self.audio_player.playsoundtrack(filepath=self.soundtrack[SoundType.INTRO][0], iterations=2, volume=0.5)
    
  def run(self, events: list[pygame.event.Event]) -> None:
    """ Primary method that runs the game.
    
    Args:
      events (list[pygame.event.Event]): The list of pygame events.
    """
    action: Optional[GameAction] = self.event_listener.process_events(events)
    
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
      self.text_elements
      )
    self.current_state = next_state

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

  def detect_match(self, items: Group, item_to_match: ItemSprite, coordinates) -> bool:
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

  def process_point_gain(self) -> None:
    """ Increments points and controls leveling up. """
    self.current_level.increment_score(points=1)
    self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)
    self.audio_player.playsound(path=self.soundtrack[SoundType.EFFECTS][0], volume=1.0) # mark sound as not playing

  def end_turn(self) -> ProcessPointResult:
    if self.current_level.is_completed():
      self.audio_player.playsound(path=self.soundtrack[SoundType.EFFECTS][1], volume=1.0)
      return ProcessPointResult.LEVEL_COMPLETED
    else:
      return ProcessPointResult.TURN_COMPLETED

  def level_up(self) -> None:
    """ Levels up the game."""
    logger.info('level up')
    # level_number is 1 based
    self.set_current_level(level_number=self.current_level.level_number + 1)
    # play hand clap sound effect
    # self.audio_player.playsound(sound='audio/level_up.wav', vol=0.5)

  def set_current_level(self, level_number: int) -> None:
    """ Sets the current level and updates the text element related to displaying the level number.
    
    Args:
      level_number (int): The level number.
    """
    self.current_level = self.levels[level_number - 1]
    self.text_elements[TextElementType.LEVEL_UP].set_text(f'Level {level_number}')

  def transition_to_next_level(self) -> bool:
    """ Transitions to the next level.
    
    Returns:
      bool: True if the transition is complete, False otherwise.
    """
    if self.text_elements[TextElementType.LEVEL_UP].current_position[0] < SCREEN_WIDTH + 100:
      self.animation_engine.add_animation(TextTransition(self.text_elements[TextElementType.LEVEL_UP], x_increment=12, y_increment=0)).execute()
      return False
    else:
      # update UI elements
      self.text_elements[TextElementType.LEVEL_UP].reset_to_start_position()
      self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)
      pygame.time.delay(ANIMATION_DELAY)
      return True

  def reset_game_levels(self):
    """ Resets the game levels."""
    for level in self.levels:
      level.reset()
    self.set_current_level(level_number=1)

  def completed_all_levels(self) -> bool:
    """ Returns True if all levels have been completed, False otherwise."""
    return self.current_level.level_number == len(self.levels)

  def display_game_completed(self) -> bool:
    """ Displays the game completed text element.
    
    Returns:
      bool: True if the transition is complete, False otherwise.
    """
    if self.text_elements[TextElementType.GAME_COMPLETED].current_position[0] < (SCREEN_WIDTH - self.text_elements[TextElementType.GAME_COMPLETED].surface.get_width()) / 2:
      self.animation_engine.add_animation(TextTransition(self.text_elements[TextElementType.GAME_COMPLETED], x_increment=7, y_increment=0)).execute()
      return False
    else:
      self.text_elements[TextElementType.GAME_COMPLETED].reset_to_start_position()
      return True

  def prepare_sprites_for_new_turn(self) -> None:
    """ Generates sprites for a new puzzle and scales them down."""
    self.item_to_match, self.items = self.current_level.puzzle.generate()
    for sprite in [self.item_to_match] + self.items.sprites():
      self.animation_engine.add_animation(ScaleSprite(scaling_factor=-100, sprite=sprite))
    self.animation_engine.execute()

  def transition_to_next_turn(self, items: Group, item_to_match: ItemSprite) -> bool:
    """ Scales sprites down, kills sprites, and updates UI.
    
    Args:
      items (Group): The group of sprites.
      item_to_match (ItemSprite): The item to match.
    """
    # play some sound effect to indicate success
    # self.audio_player.playsound(sound='audio/incorrect.wav', vol=0.5)
    # play the word for the item that was matched
    # self.audio_player.playsound(sound='audio/correct.wav', vol=0.5)
    
    all_sprites: list[ItemSprite] = [item_to_match] + items.sprites()
    if any(sprite.scale > 0 for sprite in all_sprites):
      for sprite in [item_to_match] + items.sprites():
        self.animation_engine.add_animation(ScaleSprite(scaling_factor=-8, sprite=sprite))
      self.animation_engine.execute()
      return False
    else: 
      self.kill_sprites()
      pygame.time.delay(ANIMATION_DELAY)
      return True

  def start_new_turn(self) -> bool:
    """ Generates sprites and spans them in to create a new puzzle
    
      Returns:
        bool: True if the sprites were successfully spawned, False otherwise.
    """
    if len(self.items) == 0:
      self.prepare_sprites_for_new_turn()
    return self.spawn_sprites(self.items, self.item_to_match)
  
  def spawn_sprites(self, items: Group, item_to_match: ItemSprite) -> bool:
    """ Scales sprites in to create a spawn effect.
    
    Args:
      items (Group): The group of sprites.
      item_to_match (ItemSprite): The item to match.
      
    Returns:
      bool: True if the sprites were successfully scaled in, False otherwise.
    """
    all_sprites: list[ItemSprite] = [item_to_match] + items.sprites()
    if any(sprite.scale < 100 for sprite in all_sprites):
      for sprite in all_sprites:
        self.animation_engine.add_animation(ScaleSprite(scaling_factor=10, sprite=sprite))
      self.animation_engine.execute()
      return False
    else:
      return True

  def kill_sprites(self) -> None:
    """ Remove all sprites."""
    if(self.item_to_match):
      SpriteHandler.kill_sprite(self.item_to_match)
    if(self.items):
      SpriteHandler.kill_sprite_group(self.items)

  def quit(self) -> None:
    """ Quits game and exits program. """
    logger.info('quitting game')
    pygame.quit()
    sys.exit()