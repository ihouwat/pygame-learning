from dataclasses import dataclass
import pygame

@dataclass(kw_only=True, eq=True)
class Item(pygame.sprite.Sprite):
  image: pygame.Surface
  # sound: pygame.mixer.Sound
  word: str
  text_identifier: str
  
  def __post_init__(self):
    super().__init__()
    self.rect = self.image.get_rect()
  
  # By default, dataclass() will not implicitly add a __hash__() method unless it is safe to do so.
  # we add this method in order to use instances of the class in pygame sprite groups
  def __hash__(self) -> int:
    return hash((self.text_identifier, self.word, self.image))
  
  def update_rect(self, x: int, y: int):
    self.rect.x = x
    self.rect.y = y


# data class for the pure item to create
# @dataclass(kw_only=True, eq=True)
# class Itemx():
#   image_path: str
#   # sound_path: pygame.mixer.Sound
#   word: str
#   text_identifier: str