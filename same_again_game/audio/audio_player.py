from pygame import mixer


class AudioPlayer:
	def __init__(self):
		self.volume = 0.5 # default volume
		
	def playsoundtrack(self, music, num, vol):
		mixer.music.set_volume(vol)
		mixer.music.load(music)
		mixer.music.play(num)

	def playsound(self, sound, vol):
		sound.set_volume(vol)
		sound.play()

	def stop(self):
		mixer.music.stop()