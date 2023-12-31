from funcs import get_file
from pygame import mixer


class AudioPlayer:
		
	def playsoundtrack(self, filepath: str, iterations: int, volume: float = 0.5):
		track = self.load_music(filepath)
		mixer.music.set_volume(volume)
		mixer.music.load(track)
		mixer.music.play(iterations)

	def playsound(self, sound, vol):
		sound.set_volume(vol)
		sound.play()

	def stop(self):
		mixer.music.stop()
	
	def load_music(self, path) -> str:
		return get_file('assets', 'music', path)