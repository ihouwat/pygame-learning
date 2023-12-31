import pygame
from config.logger import logger
from engine.animations import SpriteHoverEffect
from models.game_state_machine import GameContext, GameStateMachine
from models.game_types import GameAction, GameState, ProcessPointResult


class MenuOpenState(GameStateMachine):
	""" MenuOpenState is responsible for handling the game logic when the menu is open. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if self.action == GameAction.START_NEW_GAME:
			self.game_instance.kill_sprites()
			self.game_instance.reset_game_levels()			
			self.game_instance.save_user_settings(self.events[0])
			#play soundtrack
			# self.audio_player.playsoundtrack(music='audio/soundtrack.mp3', num=-1, vol=0.5)
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

class LevelCompletedState(GameStateMachine):
	""" LevelCompletedState is responsible for handling the game logic when a level is completed. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		if not self.game_instance.transition_to_next_turn(self.items, self.item_to_match):
			return GameState.LEVEL_COMPLETED
		if self.game_instance.completed_all_levels():
			return GameState.GAME_COMPLETED
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
		self.game_instance.animation_engine.add_animation(
			SpriteHoverEffect(items=self.items, min_scale=100, max_scale=125)
		).execute()
		if self.action == GameAction.MOUSE_EXITED_WINDOW:
			return GameState.PAUSED
		if self.action == GameAction.OPEN_MENU:
			return GameState.MENU_IS_OPEN
		if self.action == GameAction.ITEM_SELECTED:
			match = self.game_instance.match_detected(self.items, self.item_to_match, pygame.mouse.get_pos())
				logger.info('match detected!')
				result: ProcessPointResult = self.game_instance.process_point_gain()
				if result == ProcessPointResult.LEVEL_COMPLETED:
					return GameState.LEVEL_COMPLETED
				else:
					return GameState.TRANSITION_TO_NEXT_TURN
		
		return GameState.PLAYING

class GameCompletedState(GameStateMachine):
	""" GameCompletedState is responsible for handling the game logic when the game is completed. """
	def __init__(self, game_context: GameContext):
		super().__init__(game_context)
	
	def execute(self) -> GameState:
		# play a big cheer sound effect
		# self.audio_player.playsound(sound='audio/game_completed.wav', vol=0.5)

		if not self.game_instance.display_game_completed():
			return GameState.GAME_COMPLETED
		# quit the game
		logger.info('You have completed all levels!')
		pygame.time.wait(3000)
		self.game_instance.quit()
		return GameState.GAME_COMPLETED
