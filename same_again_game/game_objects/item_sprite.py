from dataclasses import dataclass
from typing import Optional

import pygame
from models.item_config import ItemConfig


@dataclass(kw_only=True)
class ItemSprite(pygame.sprite.Sprite):
  """ Represents an item sprite.
  
  Attributes:
    image(pygame.Surface): The image of the item.
    word(str): The word that the item represents.
    text_identifier(str): The text identifier of the item.
    sound(pygame.mixer.Sound): The sound of the word representing the item.
  """
  image: pygame.Surface
  # sound: pygame.mixer.Sound
  word: str
  text_identifier: str
  metadata: Optional[ItemConfig] = None
  
  def __post_init__(self):
    super().__init__()
    self.rect = self.image.get_rect()

  # By default, dataclass() will not implicitly add a __hash__() method unless it is safe to do so.
  # we add this method in order to use instances of the class in pygame sprite groups
  def __hash__(self) -> int:
    return hash((self.metadata))

  @classmethod
  # 'ItemSprite' is a forward reference, a string that contains the class name of a class that hasn't been fully defined at the point we're adding the type hint
  def create_from(cls, sprite: 'ItemSprite') -> 'ItemSprite':
    """ Creates a copy of an item sprite."""
    return cls(image=sprite.image, text_identifier=sprite.text_identifier, word=sprite.word, metadata=sprite.metadata)

  def update(self, x: int, y: int):
    self.rect.x = x
    self.rect.y = y
