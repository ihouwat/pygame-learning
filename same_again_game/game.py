
import sys
from typing import Optional

import pygame
from audio.audio_player import AudioPlayer
from config.logger import logger
from config.settings import FONT_NAME, FONT_REGULAR, SCREEN_HEIGHT, SCREEN_WIDTH
from engine.event_listener import EventListener
from engine.renderer import Renderer
from engine.sprite_handler import SpriteHandler
from game_objects.item_sprite import ItemSprite
from game_objects.level import Level
from models.game_types import Color, GameAction, GameState, Language, ProcessPointResult
from pygame.sprite import Group
from ui.game_menu import GameMenu
from ui.status_bar import StatusBar
from ui.ui_display import UIDisplay


class Game:
  """ Represents a game of Same Again.
  
  Attributes:
    renderer(Renderer): The game renderer.
    audio_player(AudioPlayer): The audio player.
    event_listener(EventListener): The event listener.
    status_bar(StatusBar): The status bar.
    game_menu(GameMenu): The game menu.
    levels(list[Level]): The levels of the game.
    current_level(Level): The current level of the game.
    selected_language(Language): The selected language of the game.
    player_name(str): The name of the player.
    game_state(GameState): The state of the game.
    ui_display(UIDisplay): The UI display.
  """

  def __init__(self, renderer: Renderer, audio_player: AudioPlayer, event_listener: EventListener, status_bar: StatusBar, game_menu: GameMenu, levels: list[Level], language: Language):
    self.renderer: Renderer = renderer
    self.audio_player = audio_player
    self.event_listener: EventListener = event_listener
    self.status_bar: StatusBar = status_bar
    self.game_menu: GameMenu = game_menu
    self.levels: list[Level] = levels
    
    # game state (candidates for extraction)
    self.current_level: Level = self.levels[0]
    self.selected_language: Language = language
    self.player_name: str = "Player"
    self.game_state: GameState = GameState.MENU_OPEN

    # ui display state
    self.ui_display = UIDisplay(language=language, player_name=self.player_name, score=self.current_level.score, level=self.current_level.level_number)

  def run(self, events: list[pygame.event.Event]) -> None:
    """ Primary method that runs the game.
    
    Args:
      events (list[pygame.event.Event]): The list of pygame events.
    """
    action: Optional[GameAction] = self.event_listener.process_events(events)
    items: Group = self.current_level.puzzle.items
    item_to_match: ItemSprite = self.current_level.puzzle.item_to_match
    
    if action == GameAction.QUIT:
      self.quit()
    
    if self.game_state == GameState.MENU_OPEN:

      if action == GameAction.START_NEW_GAME:
        for level in self.levels:
          level.reset()
        self.current_level = self.levels[0]
        self.save_user_settings(events[0])
        self.animate_level_transition() 
        
        #play soundtrack
        # self.audio_player.playsoundtrack(music='audio/soundtrack.mp3', num=-1, vol=0.5)
        
        self.start_new_turn()
        self.game_state = GameState.PLAYING

      if action == GameAction.RESUME_GAME:
        self.save_user_settings(events[0])
        self.game_state = GameState.PLAYING
      
      else:
        if not self.game_menu.menu.is_enabled():
          self.game_menu.open_menu()
        self.renderer.draw_game_menu(self.game_menu)
        self.game_menu.menu.update(events)

    elif self.game_state == GameState.PAUSED:
      if action == GameAction.MOUSE_ENTERED_WINDOW:
        self.game_state = GameState.PLAYING
    
    elif self.game_state == GameState.TRANSITION_TO_NEXT_TURN:
      self.transition_to_next_turn(items, item_to_match)
      self.game_state = GameState.START_NEW_TURN
    
    elif self.game_state == GameState.START_NEW_TURN:
      self.start_new_turn()
      self.game_state = GameState.PLAYING
    
    elif self.game_state == GameState.LEVEL_COMPLETED:
      self.transition_to_next_turn(items, item_to_match)
      self.level_up()
      
      self.start_new_turn()
      self.game_state = GameState.PLAYING
    
    elif self.game_state == GameState.GAME_COMPLETED:
      logger.info('You have completed all levels!')
      # play a big cheer sound effect
      # self.audio_player.playsound(sound='audio/game_completed.wav', vol=0.5)
      self.quit()
    
    elif self.game_state == GameState.PLAYING:
      if action == GameAction.MOUSE_EXITED_WINDOW:
        self.game_state = GameState.PAUSED
      if action == GameAction.OPEN_MENU:
        self.game_menu.open_menu()
        self.game_state = GameState.MENU_OPEN
      if action == GameAction.SELECT:
        if(self.match_detected(items, item_to_match, pygame.mouse.get_pos())):
          logger.info('match detected')
          result: ProcessPointResult = self.process_point_gain()
          if result == ProcessPointResult.LEVEL_COMPLETED:
            if(self.completed_all_levels()):
              self.game_state = GameState.GAME_COMPLETED
            else:
              self.game_state = GameState.LEVEL_COMPLETED
          else:
            self.game_state = GameState.TRANSITION_TO_NEXT_TURN

      # scale sprites on hover
      item_sprites: list[ItemSprite] = items.sprites()
      for sprite in item_sprites:
        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
          if sprite.scale < 125:
            sprite.scale_by(scaling_factor=6)
        else:
          if sprite.scale > 100:
            sprite.scale_by(scaling_factor=-7)

      self.renderer.draw(item_to_match=item_to_match, items=items, status_bar=self.status_bar, ui_display=self.ui_display)

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
    self.animate_level_transition()

  def animate_level_transition(self):
      self.ui_display.update(player=self.player_name, score=self.current_level.score, level=self.current_level.level_number, language=self.selected_language)
      font = pygame.font.Font(pygame.font.match_font(FONT_NAME), FONT_REGULAR)
      text_color = pygame.Color(Color.WHITE.value)
      text = font.render(f'Level {self.current_level.level_number}', True, text_color)
      y = (SCREEN_HEIGHT // 2) - FONT_REGULAR
      x = 0 - FONT_REGULAR

      pygame.time.wait(250)
      while x < SCREEN_WIDTH + 100:
        self.renderer.render_level_transition_animation(text, (x, y), self.status_bar, self.ui_display)
        x += 1
        pygame.display.flip()

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
    pygame.time.wait(350)
    # scale sprites down to prepare for spawn in
    self.scale_sprites(scaling_factor=-100, items=items, item_to_match=item_to_match)
    # spawn in sprites
    self.scale_sprites(scaling_factor=5, items=items, item_to_match=item_to_match, draw_transitions=True)

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
    self.scale_sprites(scaling_factor=-5, items=items, item_to_match=item_to_match, draw_transitions=True)
    self.kill_sprites()

  def kill_sprites(self) -> None:
    """ Remove all sprites."""
    if(self.current_level.puzzle.item_to_match):
      SpriteHandler.kill_sprite(self.current_level.puzzle.item_to_match)
    if(self.current_level.puzzle.items):
      SpriteHandler.kill_sprite_group(self.current_level.puzzle.items)

  def scale_sprites(self, scaling_factor: float, items: Group, item_to_match: ItemSprite, draw_transitions: bool = False) -> None:
    """ Scales sprites up or down.

    Args:
      scaling_factor (float): The amount to scale the sprite by.
      items (Group): The group of sprites to scale.
      item_to_match (ItemSprite): The item to match.
      draw_transitions (bool): Whether or not to draw the transitions. Defaults to False.
    """
    sprites: list[ItemSprite] = [item_to_match] + items.sprites()

    def execute_animation():
      self.animate_sprite_scale(scaling_factor=scaling_factor, sprite=sprite, item_to_match=item_to_match, items=items, draw_transitions=draw_transitions)

    for sprite in sprites:
      if scaling_factor < 0:
        while sprite.scale > 0:
          execute_animation()
        pygame.time.wait(10)
      else:
        while sprite.scale < 100:
          execute_animation()
        pygame.time.wait(10)
  
  def animate_sprite_scale(self, scaling_factor: float, sprite: ItemSprite, items: Group, item_to_match: ItemSprite, draw_transitions: bool = False) -> None:
    sprite.scale_by(scaling_factor=scaling_factor)
    if draw_transitions:
      self.renderer.draw(item_to_match=item_to_match, items=items, status_bar=self.status_bar, ui_display=self.ui_display)
    pygame.display.update()

  def quit(self) -> None:
    """ Quits game and exits program. """
    logger.info('quitting game')
    pygame.quit()
    sys.exit()