import pygame
from config.logger import logger
from config.settings import ENTERED_WRONG_ANSWER, MATCH_DETECTED
from models.game_state_machine import GameContext, StateMachine
from models.game_types import (
	GameAction,
	GameState,
	MatchResult,
	NextTurnStatus,
)


class MenuOpenState(StateMachine):
	""" MenuOpenState is responsible for handling the game logic when the menu is open. """
	
	def execute(self, context: GameContext) -> GameState:
		if context.action == GameAction.START_NEW_GAME:
			context.game.save_user_settings(context.events[0])
			context.game.start_new_game()
			return GameState.TRANSITION_TO_NEXT_LEVEL

		if context.action == GameAction.RESUME_GAME:
			context.game.save_user_settings(context.events[0])
			return GameState.PLAYING

		else:
			if not context.game.game_menu.menu.is_enabled():
				context.game.game_menu.open_menu()
			context.game.game_menu.menu.update(context.events)
			return GameState.MENU_IS_OPEN

class PausedState(StateMachine):
	""" PausedState is responsible for handling the game logic when the game is paused. """
	
	def execute(self, context: GameContext) -> GameState:
		if context.action == GameAction.MOUSE_ENTERED_WINDOW:
			return GameState.PLAYING
		return GameState.PAUSED

class TransitionTurnsState(StateMachine):
	""" TransitionTurnsState is responsible for handling the game logic when transitioning between turns. """
	
	def execute(self, context: GameContext) -> GameState:
		if context.game.transition_to_next_turn(context.items, context.item_to_match):
			return GameState.START_NEW_TURN
		return GameState.TRANSITION_TO_NEXT_TURN

class StartNewTurnState(StateMachine):
	""" StartNewTurnState is responsible for handling the game logic when starting a new turn. """
	
	def execute(self, context: GameContext) -> GameState:
		if context.game.start_new_turn():
			return GameState.PLAYING
		return GameState.START_NEW_TURN

class EndTurnState(StateMachine):
	""" EndTurnState is responsible for handling the game logic when ending a turn. """
	
	def execute(self, context: GameContext) -> GameState:
		result: NextTurnStatus = context.game.end_turn()
		if result == NextTurnStatus.LEVEL_COMPLETED:
			return GameState.LEVEL_COMPLETED
		elif result == NextTurnStatus.GAME_COMPLETED:
			return GameState.GAME_COMPLETED
		else:
			return GameState.TRANSITION_TO_NEXT_TURN

class LevelCompletedState(StateMachine):
	""" LevelCompletedState is responsible for handling the game logic when a level is completed. """
	
	def execute(self, context: GameContext) -> GameState:
		if not context.game.transition_to_next_turn(context.items, context.item_to_match):
			return GameState.LEVEL_COMPLETED
		context.game.level_up()
		return GameState.TRANSITION_TO_NEXT_LEVEL

class TransitionLevelState(StateMachine):
	""" TransitionLevelState is responsible for handling the game logic when transitioning between levels. """
	
	def execute(self, context: GameContext) -> GameState:
		if context.game.transition_to_next_level():
			return GameState.START_NEW_TURN
		return GameState.TRANSITION_TO_NEXT_LEVEL

class PlayingState(StateMachine):
	""" PlayingState is responsible for handling the game logic when the game is playing. """
	def __init__(self):
		super().__init__()
	
	def execute(self, context: GameContext) -> GameState:
		context.game.process_playing_animation()
		if context.action == GameAction.MOUSE_EXITED_WINDOW:
			return GameState.PAUSED
		if context.action == GameAction.OPEN_MENU:
			return GameState.MENU_IS_OPEN
		if context.action == GameAction.ITEM_SELECTED:
			match: MatchResult = context.game.detect_match(context.items, context.item_to_match, pygame.mouse.get_pos())
			if match == MatchResult.MATCH:
				pygame.event.post(pygame.event.Event(MATCH_DETECTED))
			elif match == MatchResult.INCORRECT_MATCH:
				pygame.event.post(pygame.event.Event(ENTERED_WRONG_ANSWER))
		if context.action == GameAction.WRONG_ITEM_SELECTED:
			context.game.process_wrong_answer()
		if context.action == GameAction.MATCH_DETECTED:
				logger.info('match detected!')
				context.game.process_point_gain()
				return GameState.END_TURN

		return GameState.PLAYING

class GameCompletedState(StateMachine):
	""" GameCompletedState is responsible for handling the game logic when the game is completed. """
	
	def execute(self, context: GameContext) -> GameState:
		if not context.game.display_game_completed():
			return GameState.GAME_COMPLETED
		context.game.end_game()
		return GameState.GAME_COMPLETED
