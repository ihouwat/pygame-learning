from dataclasses import dataclass

import pygame


@dataclass
class SoundEffect:
	sound: pygame.mixer.Sound
	path: str