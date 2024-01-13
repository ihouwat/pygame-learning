
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

import pygame
from game_objects.item_sprite import ItemSprite
from models.game_types import GameAction, GameState


@dataclass
class GameContext:
	"""  Holds context for the game state machine.
	
	Attributes:
		game: The game instance.
		events: The events to be processed.
		item_to_match: The item to match.
		items: The items.
		action: The action to be processed.
	"""
	game: Any
	events: list[pygame.event.Event]
	item_to_match: ItemSprite
	items: pygame.sprite.Group
	action: Optional[GameAction] = None

class StateMachine(ABC):
	""" Abstract class for game state machines."""
	
	@abstractmethod
	def execute(self, game_context: GameContext) -> GameState:
		""" Where the game logic is executed. 

		Args:
			game_context: The game context object to be used by the state machine.

		Returns:
			The next game state.
		"""
		...
