from funcs import get_file
from pygame import mixer
import pygame

class AudioPlayer:
		
	def playsoundtrack(self, filepath: str, iterations: int, volume: float = 0.5):
		track = self.load_music(filepath)
		mixer.music.set_volume(volume)
		mixer.music.load(track)
		mixer.music.play(iterations)

	def playsound(self, path: str, volume: float):
		sound = self.load_sound(path)
		sound.set_volume(volume)
		sound.play()

	def stop(self):
		mixer.music.stop()
	
	def load_music(self, path) -> str:
		return get_file('assets', 'music', path)

	def load_sound(self, path) -> pygame.mixer.Sound:
		return pygame.mixer.Sound(get_file('assets', 'sounds', path))