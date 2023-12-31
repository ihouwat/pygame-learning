
import random
import sys
from typing import Optional

import pygame
from audio.audio_player import AudioPlayer
from config.logger import logger
from config.settings import (
  ANIMATION_DELAY,
  FONT_LARGE,
  FONT_NAME,
  SCREEN_HEIGHT,
  SCREEN_WIDTH,
  language_paths,
)
from engine.animator import Animator
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
from funcs import get_music_track_path, get_sound_effect_path, get_spoken_word_path
from game_objects.item_sprite import ItemSprite
from game_objects.level import Level
from game_objects.text_element import TextElement
from models.game_state_machine import GameContext, StateMachine
from models.game_types import (
  Color,
  GameAction,
  GameState,
  Language,
  MatchResult,
  NextTurnStatus,
  Soundtrack,
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
    animator (Animator): The animator.
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
  def __init__(self, renderer: Renderer, ui_display: UIDisplay, animator: Animator, audio_player: AudioPlayer, event_listener: EventListener, status_bar: StatusBar, game_menu: GameMenu, levels: list[Level], language: Language, soundtrack: Soundtrack):
    self.renderer: Renderer = renderer
    self.ui_display = ui_display
    self.animator = animator
    self.audio_player = audio_player
    self.event_listener: EventListener = event_listener
    self.status_bar: StatusBar = status_bar
    self.game_menu: GameMenu = game_menu
    self.levels: list[Level] = levels
    self.game_states: dict[GameState, StateMachine] = {
      GameState.PLAYING: PlayingState(),
      GameState.MENU_IS_OPEN: MenuOpenState(),
      GameState.LEVEL_COMPLETED: LevelCompletedState(),
      GameState.GAME_COMPLETED: GameCompletedState(),
      GameState.PAUSED: PausedState(),
      GameState.TRANSITION_TO_NEXT_TURN: TransitionTurnsState(),
      GameState.TRANSITION_TO_NEXT_LEVEL: TransitionLevelState(),
      GameState.START_NEW_TURN: StartNewTurnState(),
      GameState.END_TURN: EndTurnState()
    }
    
    # game state variables (candidates for extraction)
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
    self.soundtrack: Soundtrack = soundtrack
    
    # start music
    self.audio_player.playsoundtrack(get_music_track_path(self.soundtrack[SoundType.INTRO][0]), iterations=2, volume=0.25)
    
  def run(self, events: list[pygame.event.Event]) -> None:
    """ Primary method that runs the game.
    
    Args:
      events (list[pygame.event.Event]): The list of pygame events.
    """
    action: Optional[GameAction] = self.event_listener.process_events(events)
    
    if action == GameAction.QUIT:
      self.quit()
    
    game_context: GameContext = GameContext(game=self, events=events, action=action, item_to_match=self.item_to_match, items=self.items)
    next_state: GameState = self.game_states[self.current_state].execute(game_context)
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
      self.selected_language = event.language
      if len(event.player) > 0:
        self.player_name = event.player
      
      self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)

  def start_new_game(self) -> None:
    self.kill_sprites()
    self.reset_game_levels()			
    self.audio_player.playsoundtrack(get_music_track_path(random.choice(self.soundtrack[SoundType.GAME_MUSIC])), iterations=5, volume=0.2)

  def transition_to_next_turn(self, items: Group, item_to_match: ItemSprite) -> bool:
    """ Transitions sprites out, kills sprites, and updates UI.
    
    Args:
      items (Group): The group of sprites.
      item_to_match (ItemSprite): The item to match.
    
    Returns:
      bool: True if the transition is complete, False otherwise.
    """
    all_sprites: list[ItemSprite] = [item_to_match] + items.sprites()
    animation_is_complete: bool = self.animator.transition_out_sprites(all_sprites=all_sprites, scale_factor=-8)
    if animation_is_complete:
      self.kill_sprites()
    return animation_is_complete

  def kill_sprites(self) -> None:
    """ Remove all sprites."""
    if(self.item_to_match):
      SpriteHandler.kill_sprite(self.item_to_match)
    if(self.items):
      SpriteHandler.kill_sprite_group(self.items)

  def start_new_turn(self) -> bool:
    """ Generates sprites and in order to start a new turn.
        As a side effect, once the sprites are generated, we will play the spoken word.

      Returns:
        bool: True if the sprites were successfully spawned, False otherwise.
    """
    if len(self.items) == 0:
      self.prepare_sprites_for_new_turn()
    are_sprites_spawned: bool = self.spawn_sprites(self.items, self.item_to_match)
    if are_sprites_spawned:
      language: str = language_paths[self.selected_language.name]
      if self.item_to_match.metadata:
        word: str =self.item_to_match.metadata.sound
        self.audio_player.playsound(path=get_spoken_word_path(language=language, word=word), volume=1.0)
      else:
        logger.error(f"Could not find sound for item {self.item_to_match.text_identifier} in language {language}.")
    return are_sprites_spawned
  
  def prepare_sprites_for_new_turn(self) -> None:
    """ Generates sprites for a new puzzle and makes the sprites disappear to prepare for a transition in effect."""
    self.item_to_match, self.items = self.current_level.puzzle.generate()
    all_sprites: list[ItemSprite] = [self.item_to_match] + self.items.sprites()
    self.animator.transition_out_sprites(all_sprites=all_sprites, scale_factor=-100)

  def spawn_sprites(self, items: Group, item_to_match: ItemSprite) -> bool:
    """ Scales sprites in to create a spawn effect.
    
    Args:
      items (Group): The group of sprites.
      item_to_match (ItemSprite): The item to match.
      
    Returns:
      bool: True if the sprites were successfully scaled in, False otherwise.
    """
    all_sprites: list[ItemSprite] = [item_to_match] + items.sprites()
    animation_is_complete = self.animator.transition_in_sprites(all_sprites=all_sprites, scale_factor=10)
    return animation_is_complete

  def process_playing_animation(self) -> None:
    self.animator.hover_effect(items=self.items, min_scale=100, max_scale=125)

  def detect_match(self, items: Group, item_to_match: ItemSprite, coordinates) -> MatchResult:
    """ Detects if the user has selected the correct item.
    Args:
      items (Group): The group of sprites.
      item_to_match (ItemSprite): The item to match.
      coordinates (tuple): The coordinates of the mouse click.
      
    Returns:
      MatchResult: The result of the match.
    """
    selected_item: list[ItemSprite] = [sprite for sprite in items if sprite.rect.collidepoint(coordinates)]

    if selected_item:
      if selected_item[0].metadata == item_to_match.metadata:
        logger.info('this is the right answer!')
        return MatchResult.MATCH
      else:
        return MatchResult.INCORRECT_MATCH
    else: 
      return MatchResult.NO_SELECTION

  def process_point_gain(self) -> None:
    """ Increments points and controls leveling up. """
    self.current_level.increment_score(points=1)
    self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)
    self.audio_player.playsound(path=get_sound_effect_path(self.soundtrack[SoundType.EFFECTS][0]), volume=1.0)
  
  def process_wrong_answer(self) -> None:
    self.audio_player.playsound(path=get_sound_effect_path(self.soundtrack[SoundType.EFFECTS][2]), volume=1.0)

  def end_turn(self) -> NextTurnStatus:
    if self.completed_all_levels():
      self.audio_player.playsound(path=get_sound_effect_path(self.soundtrack[SoundType.EFFECTS][1]), volume=1.0)
      self.audio_player.playsoundtrack(get_music_track_path(self.soundtrack[SoundType.VICTORY][0]), iterations=1, volume=0.75)
      return NextTurnStatus.GAME_COMPLETED
    elif self.current_level.is_completed():
      self.audio_player.playsound(path=get_sound_effect_path(self.soundtrack[SoundType.EFFECTS][1]), volume=0.7)
      return NextTurnStatus.LEVEL_COMPLETED
    else:
      return NextTurnStatus.TURN_COMPLETED

  def level_up(self) -> None:
    """ Levels up the game."""
    logger.info('level up')
    # level_number is 1 based
    self.set_current_level(level_number=self.current_level.level_number + 1)

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
    animation_is_complete = self.animator.animate_text_element_if_needed(text_element=self.text_elements[TextElementType.LEVEL_UP], condition_to_animate=self.text_elements[TextElementType.LEVEL_UP].current_position[0] < SCREEN_WIDTH + 100, x_increment=10, y_increment=0)
    if animation_is_complete:
      # update UI elements
      self.text_elements[TextElementType.LEVEL_UP].reset_to_start_position()
      self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)
      pygame.time.delay(ANIMATION_DELAY)
    return animation_is_complete

  def reset_game_levels(self):
    """ Resets the game levels."""
    for level in self.levels:
      level.reset()
    self.set_current_level(level_number=1)

  def completed_all_levels(self) -> bool:
    """ Returns True if all levels have been completed, False otherwise."""
    return self.current_level.is_completed() and self.current_level.level_number == len(self.levels)

  def display_game_completed(self) -> bool:
    """ Displays the game completed text element.
    
    Returns:
      bool: True if the transition is complete, False otherwise.
    """
    animation_is_complete: bool = self.animator.animate_text_element_if_needed(text_element=self.text_elements[TextElementType.GAME_COMPLETED], condition_to_animate=self.text_elements[TextElementType.GAME_COMPLETED].current_position[0] < (SCREEN_WIDTH - self.text_elements[TextElementType.GAME_COMPLETED].surface.get_width()) / 2, x_increment=7, y_increment=0)
    if animation_is_complete:
      self.text_elements[TextElementType.GAME_COMPLETED].reset_to_start_position()
    return animation_is_complete

  def end_game(self) -> None:
    logger.info('You have completed all levels!')
    pygame.time.wait(30000)
    self.quit()

  def quit(self) -> None:
    """ Quits game and exits program. """
    logger.info('quitting game')
    pygame.quit()
    sys.exit()