from dataclasses import dataclass
from typing import Optional

import pygame
from config.game_items_catalog import create_shape
from config.settings import colors
from models.game_types import Shape
from models.item_config import ItemConfig


@dataclass(kw_only=True)
class ItemSprite(pygame.sprite.Sprite):
  """ Represents an item sprite.
  
  Attributes:
    image(pygame.Surface): The image of the item.
    word(str): The word that the item represents.
    text_identifier(str): The text identifier of the item.
    sound(pygame.mixer.Sound): The sound of the word representing the item.
    initial_size(tuple[int, int]): The original size of the image.
    current_size(tuple[int, int]): The current size of the image.
    original_image(pygame.Surface): The original image of the item.
    scale(int): The scale of the item.
  """
  image: pygame.Surface
  # sound: pygame.mixer.Sound
  word: str
  text_identifier: str
  metadata: Optional[ItemConfig] = None

  
  def __post_init__(self):
    super().__init__()
    self.rect = self.image.get_rect()
    self.initial_size = self.rect
    self.current_size = self.image.get_rect().size
    self.original_image = self.image
    self.scale_factor = 100

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

  def scale(self, scaling_factor: int) -> None:
      self.scale_factor += scaling_factor
      old_center = self.rect.center

      if self.metadata and self.metadata.type == 'Shape':
        new_width, new_height = self.scale_shape(scaling_factor)
      else:
        new_width, new_height = self.scale_image()
      
      self.rect = self.image.get_rect()
      self.rect.center = old_center
      self.current_size = (int(new_width), int(new_height))

  def scale_image(self) -> tuple[int, float]:
    """ Scales the image of the item. Calculates size difference based on original image size.
      Then adds the scaling factor to the old width to return updated width and height.
      Maintains aspect ratio."""
    old_width, old_height = self.original_image.get_size()  # use original image size
    aspect_ratio = old_width / old_height
    new_width = old_width + self.scale_factor - 100 # use total scale
    new_height = new_width / aspect_ratio  # maintain aspect ratio
    self.image = pygame.transform.smoothscale(self.original_image, (int(new_width), int(new_height)))
    return new_width, new_height

  def scale_shape(self, scaling_factor) -> tuple[int, int]:
    """ Scales the shape of the item. Calculates size difference based on original size and current size.
      Then adds the scaling factor to the size difference and returns the new width and height.
    """
    size_difference = (self.current_size[0] - self.initial_size[0], self.current_size[1] - self.initial_size[1])
    new_width = self.initial_size[0] + size_difference[0] + scaling_factor
    new_height = self.initial_size[1] + size_difference[1] + scaling_factor
    for shape in Shape:
      if self.word == shape.value and self.metadata:
        self.image = create_shape(shape, colors[self.metadata.color], new_width, new_height)
    return new_width, new_height