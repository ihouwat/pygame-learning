from dataclasses import dataclass
import pygame

@dataclass(frozen=True, kw_only=True)
class Item(pygame.sprite.Sprite):
  image: pygame.Surface
  sound: pygame.mixer.Sound
  text_identifier: str
  description: str