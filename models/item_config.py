from dataclasses import dataclass

from models.game_types import Color, RealWorldObjectCategory, Shape
from models.image_source import ImageSource


@dataclass(eq=True)
class ItemConfig():
  """ Represents metadata for items that are the basis to create sprites."""
  text_identifier: str
  image: ImageSource
  sound: str
  word: str
  color: Color
  type: RealWorldObjectCategory | Shape

  def __hash__(self) -> int:
    return hash((self.text_identifier, self.image, self.sound, self.word, self.color, self.type))