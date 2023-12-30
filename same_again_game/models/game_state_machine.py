
from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional

import pygame
from game_objects.item_sprite import ItemSprite
from models.game_types import GameAction, GameState


@dataclass
class GameContext:
	"""  Holds context for the game state machine.
	
	Attributes:
		game_instance: The game instance.
		events: The events to be processed.
		item_to_match: The item to match.
		items: The items.
		action: The action to be processed.
	"""
	game_instance: Any
	events: list[pygame.event.Event]
	item_to_match: ItemSprite
	items: pygame.sprite.Group
	action: Optional[GameAction] = None

class GameStateMachine(ABC):
	""" Abstract class for game state machines. 
	
	Attributes:
		game_instance: The game instance.
		events: The events to be processed.
		item_to_match: The item to match.
		items: The items.
		action: The action to be processed.
	"""
	def __init__(self, game_context: GameContext):
		self.game_instance = game_context.game_instance
		self.action = game_context.action
		self.events = game_context.events
		self.item_to_match = game_context.item_to_match
		self.items = game_context.items

	def execute(self) -> GameState:
		""" Where the game logic is executed. 

		Returns:
			The next game state.
		"""
		...
