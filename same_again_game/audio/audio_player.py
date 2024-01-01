import pygame
from funcs import get_file
from models.sound_effect import SoundEffect
from pygame import mixer


class AudioPlayer:
	def __init__(self) -> None:
		mixer.init(frequency=44100)
		self.sound_effects: list[SoundEffect] = []
		
	def playsoundtrack(self, filepath: str, iterations: int, volume: float = 0.5):
		track = self.load_music(filepath)
		mixer.music.set_volume(volume)
		mixer.music.load(track)
		mixer.music.play(iterations)

	def stop_music(self) -> None:
		mixer.music.stop()
	
	def playsound(self, path: str, volume: float) -> None:
		sound, cached_sound = self.load_and_cache_sound(path)

		if cached_sound.is_playing:
			return

		sound.set_volume(volume)
		sound.play()
		cached_sound.is_playing = True

	def load_and_cache_sound(self, path: str) -> tuple[pygame.mixer.Sound, SoundEffect]:
		sound: pygame.mixer.Sound
		cached_sound: SoundEffect | None = self.get_cached_sound(path)

		if cached_sound:
			sound = pygame.mixer.Sound(cached_sound.sound)
		else:
			sound = self.load_sound(path)
			cached_sound = SoundEffect(sound=sound, path=path, is_playing=False)
			self.sound_effects.append(cached_sound)

		return sound, cached_sound

	def get_cached_sound(self, path: str) -> SoundEffect | None:
		return next((s for s in self.sound_effects if s.path == path), None) # next() returns the next item in an iterator

	def stop_sound(self, path: str) -> None:
		cached_sound = self.get_cached_sound(path)
		if cached_sound is not None:
			cached_sound.sound.stop()
			cached_sound.is_playing = False
	
	def load_music(self, path) -> str:
		return get_file('assets', 'music', path)

	def load_sound(self, path) -> pygame.mixer.Sound:
		return pygame.mixer.Sound(get_file('assets', 'sounds', path))