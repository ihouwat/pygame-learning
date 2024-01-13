from dataclasses import dataclass

from models.game_types import Language


@dataclass(kw_only=True)
class UIDisplay:
	""" Represents the UI display.

	Attributes:
		language(Language): The language of the game.
		player_name(str): The name of the player.
		score(int): The score of the player.
		level(int): The level of the player.
	"""
	language: Language = Language.ENGLISH
	player_name: str = ""
	score: int = 0
	level: int = 1
	
	def update(self, player: str, score: int, level: int, language: Language) -> None:
		"""Updates the UI display."""
		self.player_name = player
		self.score = score
		self.level = level
		self.language = language