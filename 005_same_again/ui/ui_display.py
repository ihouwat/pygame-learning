from dataclasses import dataclass

from models.types import Language


@dataclass(kw_only=True)
class UIDisplay:
	language: Language
	player_name: str
	score: int
	level: int
	
	def update(self, player: str, score: int, level: int, language: Language) -> None:
		self.player_name = player
		self.score = score
		self.level = level
		self.language = language