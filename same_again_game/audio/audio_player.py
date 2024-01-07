import pygame
from funcs import load_pygame_sound
from models.sound_effect import SoundEffect
from pygame import mixer


class AudioPlayer:
	def __init__(self) -> None:
		mixer.init(frequency=44100)
		self.sound_effects: list[SoundEffect] = []
		
	def playsoundtrack(self, filepath: str, iterations: int, volume: float = 0.5):
		mixer.music.set_volume(volume)
		mixer.music.load(filepath)
		mixer.music.play(iterations)

	def stop_music(self) -> None:
		mixer.music.stop()
	
	def playsound(self, path: str, volume: float) -> None:
		sound = self.load_and_cache_sound(path)
		sound.set_volume(volume)
		sound.play()

	def load_and_cache_sound(self, path: str) -> pygame.mixer.Sound:
		sound: pygame.mixer.Sound
		cached_sound: SoundEffect | None = self.get_cached_sound(path)

		if cached_sound:
			sound = cached_sound.sound
		else:
			sound = load_pygame_sound(path)
			new_sound_effect = SoundEffect(sound=sound, path=path)
			self.sound_effects.append(new_sound_effect)

		return sound

	def get_cached_sound(self, path: str) -> SoundEffect | None:
		return next((s for s in self.sound_effects if s.path == path), None) # next() returns the next item in an iterator