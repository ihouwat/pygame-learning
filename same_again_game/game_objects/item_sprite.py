from dataclasses import dataclass
from typing import Optional

import pygame
from config.logger import logger
from config.settings import colors
from funcs import create_shape
from models.game_types import Shape
from models.item_config import ItemConfig


@dataclass(kw_only=True)
class ItemSprite(pygame.sprite.Sprite):
  """ Represents an item sprite.
  
  Attributes:
    image(pygame.Surface): The image of the item.
    word(str): The word that the item represents.
    text_identifier(str): The text identifier of the item.
    initial_size(tuple[int, int]): The original size of the image.
    current_size(tuple[int, int]): The current size of the image.
    original_image(pygame.Surface): The original image of the item.
    scale(int): The scale of the item.
  """
  image: pygame.Surface = pygame.Surface((0, 0))
  text_identifier: str = ""
  metadata: Optional[ItemConfig] = None

  def __post_init__(self):
    super().__init__()
    self.rect: pygame.Rect = self.image.get_rect()
    self.initial_size: tuple[int, int] = self.image.get_rect().size
    self.current_size: tuple[int, int] = self.image.get_rect().size
    self.original_image: pygame.Surface = self.image
    self.scale: float = 100

  # By default, dataclass() will not implicitly add a __hash__() method unless it is safe to do so.
  # we add this method in order to use instances of the class in pygame sprite groups
  def __hash__(self) -> int:
    return hash((self.metadata))

  @classmethod
  # 'ItemSprite' is a forward reference, a string that contains the class name of a class that hasn't been fully defined at the point we're adding the type hint
  def create_from(cls, sprite: 'ItemSprite') -> 'ItemSprite':
    """ Creates a copy of an item sprite."""
    return cls(image=sprite.image, text_identifier=sprite.text_identifier, metadata=sprite.metadata)

  def update(self, x: int, y: int):
    self.rect.x = x
    self.rect.y = y

  def scale_by(self, scaling_factor: float) -> bool:
    """ Scales the item sprite.
      Algorithm vary by type of item sprite.
      
      Args:
        scaling_factor(int): The amount to scale the item sprite.
      
      Returns:
        bool: True if the item sprite was successfully scaled, False otherwise.
    """
    old_center = self.rect.center

    try:
      if self.metadata and self.metadata.type == Shape:
        new_width, new_height = self.scale_shape(scaling_factor)
      else:
        new_width, new_height = self.scale_image(scaling_factor)
    except ValueError:
      logger.warning('Cannot scale item sprite any further.')
      return False

    self.rect = self.image.get_rect()
    self.rect.center = old_center
    self.current_size = (int(new_width), int(new_height))

    # update scale factor
    self.scale = self.current_size[0] / self.initial_size[0] * 100
    return True

  def scale_image(self, scaling_factor: float) -> tuple[float, float]:
    """ Scales the image of the item. Calculates size difference based on original image size.
      Then adds the scale factor to the old width to return updated width and height.
      Maintains aspect ratio.
      
    Args:
      scaling_factor(int): The amount to scale the item sprite.
    
    Returns:
      tuple[float, float]: The new width and height of the item sprite.
    """
    old_width, old_height = self.original_image.get_size()  # use original image size
    aspect_ratio = old_width / old_height

    new_scale_factor: float
    if scaling_factor < 0:
      # If scaling factor is negative, subtract it from the current scale factor
      new_scale_factor = self.scale - abs(scaling_factor)
    else:
      # If scaling factor is positive, add it to the current scale factor
      new_scale_factor = self.scale + scaling_factor

    # Ensure the new scale factor is not less than 0
    new_scale_factor = max(new_scale_factor, 0)

    new_width = old_width * (new_scale_factor / 100)  # calculate new width
    new_height = new_width / aspect_ratio  # maintain aspect ratio
    self.image = pygame.transform.smoothscale(self.original_image, (int(new_width), int(new_height)))
    return new_width, new_height

  def scale_shape(self, scaling_factor: float) -> tuple[float, float]:
    """ Scales the shape of the item. Calculates size difference based on original size and current size.
      Then adds a scaling factor to the size difference and returns the new width and height.
    
    Args:
      scaling_factor(int): The amount to scale the item sprite.
    
    Returns:
      tuple[int, int]: The new width and height of the item sprite.
    """
    
    new_scale_factor: float
    if scaling_factor < 0 and abs(scaling_factor) > self.current_size[0]:
      new_scale_factor = -self.current_size[0]
    else:
      new_scale_factor = scaling_factor

    size_difference = (self.current_size[0] - self.initial_size[0], self.current_size[1] - self.initial_size[1])
    new_width = self.initial_size[0] + size_difference[0] + new_scale_factor
    new_height = self.initial_size[1] + size_difference[1] + new_scale_factor
    for shape in Shape:
      if self.text_identifier == shape.value and self.metadata:
        self.image = create_shape(shape, colors[self.metadata.color], new_width, new_height)
    return new_width, new_height