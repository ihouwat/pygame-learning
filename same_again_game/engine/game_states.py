import random

import pygame
from config.logger import logger
from config.settings import ENTERED_WRONG_ANSWER, MATCH_DETECTED
from engine.animations import SpriteHoverEffect
from funcs import get_music_track_path
from models.game_state_machine import GameContext, GameStateMachine
from models.game_types import (
	GameAction,
	GameState,
	MatchResult,
	NextTurnStatus,
	SoundType,
)


class MenuOpenState(GameStateMachine):
	""" MenuOpenState is responsible for handling the game logic when the menu is open. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if self.action == GameAction.START_NEW_GAME:
			self.game_instance.kill_sprites()
			self.game_instance.reset_game_levels()			
			self.game_instance.save_user_settings(self.events[0])
			# play music!
			self.game_instance.audio_player.playsoundtrack(get_music_track_path(random.choice(self.game_instance.soundtrack[SoundType.GAME_MUSIC])), iterations=5, volume=0.25)
			return GameState.TRANSITION_TO_NEXT_LEVEL

		if self.action == GameAction.RESUME_GAME:
			self.game_instance.save_user_settings(self.events[0])
			return GameState.PLAYING

		else:
			if not self.game_instance.game_menu.menu.is_enabled():
				self.game_instance.game_menu.open_menu()
			self.game_instance.game_menu.menu.update(self.events)
			return GameState.MENU_IS_OPEN

class PausedState(GameStateMachine):
	""" PausedState is responsible for handling the game logic when the game is paused. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if self.action == GameAction.MOUSE_ENTERED_WINDOW:
			return GameState.PLAYING
		return GameState.PAUSED

class TransitionTurnsState(GameStateMachine):
	""" TransitionTurnsState is responsible for handling the game logic when transitioning between turns. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if self.game_instance.transition_to_next_turn(self.items, self.item_to_match):
			return GameState.START_NEW_TURN
		return GameState.TRANSITION_TO_NEXT_TURN

class StartNewTurnState(GameStateMachine):
	""" StartNewTurnState is responsible for handling the game logic when starting a new turn. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if self.game_instance.start_new_turn():
			return GameState.PLAYING
		return GameState.START_NEW_TURN

class EndTurnState(GameStateMachine):
	""" EndTurnState is responsible for handling the game logic when ending a turn. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		result: NextTurnStatus = self.game_instance.end_turn()
		if result == NextTurnStatus.LEVEL_COMPLETED:
			return GameState.LEVEL_COMPLETED
		elif result == NextTurnStatus.GAME_COMPLETED:
			return GameState.GAME_COMPLETED
		else:
			return GameState.TRANSITION_TO_NEXT_TURN

class LevelCompletedState(GameStateMachine):
	""" LevelCompletedState is responsible for handling the game logic when a level is completed. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if not self.game_instance.transition_to_next_turn(self.items, self.item_to_match):
			return GameState.LEVEL_COMPLETED
		self.game_instance.level_up()
		return GameState.TRANSITION_TO_NEXT_LEVEL

class TransitionLevelState(GameStateMachine):
	""" TransitionLevelState is responsible for handling the game logic when transitioning between levels. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if self.game_instance.transition_to_next_level():
			return GameState.START_NEW_TURN
		return GameState.TRANSITION_TO_NEXT_LEVEL

class PlayingState(GameStateMachine):
	""" PlayingState is responsible for handling the game logic when the game is playing. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		self.game_instance.animation_engine.add_animation(SpriteHoverEffect(items=self.items, min_scale=100, max_scale=125)).execute()
		if self.action == GameAction.MOUSE_EXITED_WINDOW:
			return GameState.PAUSED
		if self.action == GameAction.OPEN_MENU:
			return GameState.MENU_IS_OPEN
		if self.action == GameAction.ITEM_SELECTED:
			match: MatchResult = self.game_instance.detect_match(self.items, self.item_to_match, pygame.mouse.get_pos())
			if match == MatchResult.MATCH:
				pygame.event.post(pygame.event.Event(MATCH_DETECTED))
			elif match == MatchResult.INCORRECT_MATCH:
				pygame.event.post(pygame.event.Event(ENTERED_WRONG_ANSWER))
		if self.action == GameAction.WRONG_ITEM_SELECTED:
			self.game_instance.process_wrong_answer()
		if self.action == GameAction.MATCH_DETECTED:
				logger.info('match detected!')
				self.game_instance.process_point_gain()
				return GameState.END_TURN

		return GameState.PLAYING

class GameCompletedState(GameStateMachine):
	""" GameCompletedState is responsible for handling the game logic when the game is completed. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if not self.game_instance.display_game_completed():
			return GameState.GAME_COMPLETED
		self.game_instance.end_game()
		return GameState.GAME_COMPLETED
