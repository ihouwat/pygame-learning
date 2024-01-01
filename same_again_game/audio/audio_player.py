from dataclasses import dataclass
from funcs import get_file
from pygame import mixer
import pygame

class AudioPlayer:
	def __init__(self) -> None:
		mixer.init(frequency=44100)
		self.soundtrack: list[SoundEffects] = []
		
	def playsoundtrack(self, filepath: str, iterations: int, volume: float = 0.5):
		track = self.load_music(filepath)
		mixer.music.set_volume(volume)
		mixer.music.load(track)
		mixer.music.play(iterations)

	def playsound(self, path: str, volume: float):
		sound: pygame.mixer.Sound
		
		if self.sound_is_cached(path):
			cached_sound = next(s for s in self.soundtrack if s.path == path) # next() is used by python to return the next item in an iterator
			sound = pygame.mixer.Sound(cached_sound.sound)
		else:
			sound = self.load_sound(path)
			cached_sound = SoundEffects(sound=sound, path=path)
			self.soundtrack.append(cached_sound)

		if cached_sound.is_playing:
			return

		sound.set_volume(volume)
		sound.play()
		cached_sound.is_playing = True

	def stop(self):
		mixer.music.stop()
	
	def sound_is_cached(self, path: str) -> bool:
		return bool([s for s in self.soundtrack if s.path == path])

	def stop_sound(self, path: str):
		cached_sound = next(s for s in self.soundtrack if s.path == path)
		sound: pygame.mixer.Sound = pygame.mixer.Sound(cached_sound.sound)
		sound.stop()
		cached_sound.is_playing = False

	def load_music(self, path) -> str:
		return get_file('assets', 'music', path)

	def load_sound(self, path) -> pygame.mixer.Sound:
		return pygame.mixer.Sound(get_file('assets', 'sounds', path))

@dataclass
class SoundEffects:
	sound: pygame.mixer.Sound
	path: str
	is_playing: bool = False