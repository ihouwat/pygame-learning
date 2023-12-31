import pygame
from pygame.locals import *
import sys
import random
from tkinter import * # Tkinter is a GUI library that comes with Python
import os
import pathlib
import numpy as np
from music_manager import MusicManager

def get_file(*path_args) -> str:
	file_path = os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), *path_args)
	return file_path

# util method to load images
def load_image(file_name) -> pygame.Surface:
	file_path = get_file('images', file_name)
	return pygame.image.load(file_path).convert_alpha()

def load_sound_file(file_name) -> str:
	return get_file('sounds', file_name)

def load_sound(file_name):
	file_path = load_sound_file(file_name)
	return pygame.mixer.Sound(file_path)

pygame.mixer.pre_init(44100, 16, 1, 512) 
pygame.init() # Begin pygame

# Declare variables
vec = pygame.math.Vector2 # has two components (x,y), which we'll use to track the Player sprite
HEIGHT = 350 # screen height
WIDTH = 700 # screen width
ACC = 0.3 # Acceleration
FRIC = -0.10 # Friction
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

# Setup display surface
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG") # Window title

# Custom events
hit_cooldown = pygame.USEREVENT + 1 # create a unique event we will use to implement an 'invulnerability' period after being hit by an enemy, so the player doesn't lose all their health in one frame

# music and sound
soundtrack = [load_sound_file(x) for x in ["background_village.wav", "battle_music.wav", "gameover.wav"]]
swordtrack = [load_sound("sword1.wav"), load_sound("sword2.wav")]
fsound = pygame.mixer.Sound(load_sound("fireball_sound.wav"))
hit = pygame.mixer.Sound(load_sound("enemy_hit.wav"))

# colors
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255) 

# fonts
heading_font = pygame.font.SysFont("Verdana", 40)
regular_font = pygame.font.SysFont('Corbel',25)
smaller_font = pygame.font.SysFont('Corbel',16) 
load_text = regular_font.render('LOAD' , True , color_light)

# Animation frames

# Run animation for the RIGHT
run_ani_R = [load_image(x) for x in ["Player_Sprite_R.png", "Player_Sprite2_R.png",
						"Player_Sprite3_R.png","Player_Sprite4_R.png",
						"Player_Sprite5_R.png", "Player_Sprite6_R.png",
						"Player_Sprite_R.png"]]

# Run animation for the LEFT
run_ani_L = [load_image(x) for x in ["Player_Sprite_L.png", "Player_Sprite2_L.png",
						"Player_Sprite3_L.png","Player_Sprite4_L.png",
						"Player_Sprite5_L.png", "Player_Sprite6_L.png",
						"Player_Sprite_L.png"]]

# Attack animation for the RIGHT
attack_ani_R = [load_image(x) for x in ["Player_Sprite_R.png", "Player_Attack_R.png",
								"Player_Attack2_R.png", "Player_Attack2_R.png",
								"Player_Attack3_R.png", "Player_Attack3_R.png",
								"Player_Attack4_R.png", "Player_Attack4_R.png",
								"Player_Attack5_R.png", "Player_Attack5_R.png",
								"Player_Sprite_R.png"]]

# Attack animation for the LEFT
attack_ani_L = [load_image(x) for x in ["Player_Sprite_L.png", "Player_Attack_L.png",
								"Player_Attack2_L.png", "Player_Attack2_L.png",
								"Player_Attack3_L.png", "Player_Attack3_L.png",
								"Player_Attack4_L.png", "Player_Attack4_L.png",
								"Player_Attack5_L.png", "Player_Attack5_L.png",
								"Player_Sprite_L.png"]]

# Health animation
health_ani = [load_image(x) for x in ["heart0.png","heart.png",
							"heart2.png", "heart3.png",
							"heart4.png", "heart5.png"]]

# Classes
class Background(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.bgimage = load_image('Background.png')
		self.bgY = 0
		self.bgX = 0
	
	def render(self):
		displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
		
class Ground(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = load_image('Ground.png')
		self.rect = self.image.get_rect(center = (350, 350)) # rect is a must in order to interact with other objects
	
	def render(self):
		displaysurface.blit(self.image, (self.rect.x, self.rect.y))

class HealthBar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = load_image('heart5.png')

	def render(self):
		displaysurface.blit(self.image, (10, 10))

class StatusBar(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = pygame.Surface((90, 66))
		self.rect = self.surf.get_rect(center=(500, 10))
	
	def update_draw(self):
		text1 = smaller_font.render("STAGE: " + str(handler.stage), True, color_white)
		text2 = smaller_font.render("EXP: " + str(player.experience), True, color_white)
		text3 = smaller_font.render("MANA: " + str(player.mana), True, color_white)
		text4 = smaller_font.render("FPS: " + str(int(FPS_CLOCK.get_fps())), True, color_white)

		# draw the text onto the status bar
		displaysurface.blit(text1, (585, 7))
		displaysurface.blit(text2, (585, 22))
		displaysurface.blit(text3, (585, 37))
		displaysurface.blit(text4, (585, 52))

# Pause, play, and home buttons
class PButton(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.vec = vec(620, 300)
		self.img_display = 0
	
	def render(self, num):
		if num == 0:
			self.image = load_image('home_small.png')
		elif num == 1:
			if cursor.wait == 0:
				self.image = load_image('pause_small.png')
			else:
				self.image = load_image('play_small.png')
		displaysurface.blit(self.image, (620, 300))

# Pygame doesn't support a way to detect buttons
class Cursor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = load_image('cursor.png')
		self.rect = self.image.get_rect()
		self.wait = 0
	
	def pause(self):
		if self.wait == 1:
			self.wait = 0
		else:
			self.wait = 1
	
	def hover(self):
		if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
			# if we're hovering over the buttons we're interested in, display our custom cursor image
			pygame.mouse.set_visible(False)
			cursor.rect.center = pygame.mouse.get_pos() # update position
			displaysurface.blit(cursor.image, cursor.rect)
		else:
			pygame.mouse.set_visible(True)
		
class StageDisplay(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.text = heading_font.render("Stage: " + str(handler.stage), True, color_dark)
		self.rect = self.text.get_rect()
		self.posx = -100 # initialize off screen
		self.posy = 100
		self.display = False
		self.cleared = False

	def move_display(self):
		# Create the text to be displayed
		self.text = heading_font.render("STAGE: " + str(handler.stage) , True , color_dark)
		if self.posx < 700:
			self.posx += 5
			displaysurface.blit(self.text, (self.posx, self.posy))
		else:
			self.display = False
			self.posx = -100
			self.posy = 100
	
	def stage_clear(self):
		self.text = heading_font.render("STAGE CLEARED!" , True , color_dark)
		button.img_display = 0 # swicth the button back to the home button
		if self.posx < 700:
			self.posx += 10
			displaysurface.blit(self.text, (self.posx, self.posy))
		else:
			self.cleared = False
			self.posx = -100
			self.posy = 100

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = load_image('Player_Sprite_R.png')
		self.rect = self.image.get_rect()
		self.health = 5
		self.slash = 0
	
		# Position and direction
		self.vx = 0
		self.pos = vec((340, 240)) # position
		self.vel = vec(0,0) # velocity
		self.acc = vec(0,0) # acceleration
		self.direction = "RIGHT" # direction
		self.jumping = False # jumping
		self.running = False # running
		self.move_frame = 0 # track the current grame of the character being displayed
		# Combat
		self.attacking = False
		self.cooldown = False
		self.attack_frame = 0
		self.mana = 6
		self.experience = 0
		self.magic_cooldown = False # cooldown for magic attacks
	
	def move(self):
		# Keep a constant acceleration of 0.5 in the downard direction (gravity) and this also slows us down in the absence of keypresses
		self.acc = vec(0, 0.5)

		# we can check if the players has slowed down to a certain extent 
		if abs(self.vel.x) > 0.3:
			self.running = True 
		else:
			self.running = False

		# returns the current key presses
		pressed_keys = pygame.key.get_pressed()
	
		# Accelerates the player in the direction of the key press
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = ACC

		# Formulas to calculate velocity while accounting for friction
		# Gist of it is that acceleration is calculated based off velocity and friction, and the position is updated based off how much distance was covered (based on acceleration and velocity)
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc # Updates the position with the new values

		# This causes character warping from one point of the screen to the other
		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

		# Update rect pos
		self.rect.midbottom = self.pos

	# Update one frame per game cycle
	def update(self):
		# do nothing if we are in pause mode
		if cursor.wait == 1: 
			return
		# Return to the base frame if at the end of a movement sequence
		if self.move_frame > 6: # we only have six images in the animation, the more images the smoother the animation
			self.move_frame = 0
			return

		# Move the character to the next grame if the player is running
		if self.jumping is False and self.running is True:
			# First determine the direction the player is going in
			if self.vel.x > 0: # this means the player is moving to the right
				self.image = run_ani_R[self.move_frame] # cycle through the list of images
				self.direction = "RIGHT"
			else:
				self.image = run_ani_L[self.move_frame]
				self.direction = "LEFT"
		
			self.move_frame += 1 # change the frame

		# If the player is not moving, display the idle frame so we're not stuck in a running animation
		if abs(self.vel.x) < 0.2 and self.move_frame != 0:
			self.move_frame = 0
			if self.direction == "RIGHT":
				self.image = run_ani_R[self.move_frame]
			elif self.direction == "LEFT":
				self.image = run_ani_L[self.move_frame]

	def attack(self):
		if cursor.wait == 1: # do nothing if we are in pause mode
			return
		# If attack frame has reached end of sequence, return to base frame and end the attack
		if self.attack_frame > 10:
			self.attack_frame = 0
			self.attacking = False

		# control slashing sounds
  
		if self.attack_frame == 0:
			music_manager.playsound(swordtrack[self.slash], 0.05)
			self.slash += 1
			if self.slash > 1:
				self.slash = 0

		# Check direction for correct animation to display
		if self.direction == "RIGHT":
			self.image = attack_ani_R[self.attack_frame]
		elif self.direction == "LEFT":
			self.attack_correction()
			self.image = attack_ani_L[self.attack_frame]
	
		# Update the attack frame
		self.attack_frame += 1
	
	# Pygame doesn't support individual entities and non-rectangle collision detection.
	# So when we turn our character from righ tto left and attack, the center point of the image changes, pushing the player back.
	def attack_correction(self):
		# correct an error with character position on the left attack frames
		if self.attack_frame == 1:
			self.pos.x -= 20
		if self.attack_frame == 10:
			self.pos.x += 20

	def jump(self):
		# the self.rect.x += 1 and self.rect.x -= 1 is there to check for collisions on the x-axis
		self.rect.x += 1

		# Check to see if the player is on the ground
		hits = pygame.sprite.spritecollide(self, ground_group, False)

		self.rect.x -= 1
	
		# If touching the ground, and not currently jumping, cause the player to jump
		if hits and not self.jumping:
			self.jumping = True
			self.vel.y = -12 # negative y velocity means upwards

	def gravity_check(self):
		hits = pygame.sprite.spritecollide(player, ground_group, False)
		if self.vel.y > 0: # check if the player has downwards velocity, meaning they are falling
			if hits: # if there is a collision between the player and the ground
				lowest = hits[0]
				if self.pos.y < lowest.rect.bottom:
					self.pos.y = lowest.rect.top + 1
					self.vel.y = 0 # stop the player from falling
					self.jumping = False # allow the player to jump again

	def player_hit(self):
		if self.cooldown is False:
			self.cooldown = True # enable the cooldown
			pygame.time.set_timer(hit_cooldown, 1000) # Reset the cooldown in 1 second
			
			self.health = self.health - 1
			health.image = health_ani[self.health]
			music_manager.playsound(hit, 0.15)
			print("Player was hit")

			if self.health == 0:
				print("Player died")
				self.kill()
				music_manager.stop()
				music_manager.playsoundtrack(soundtrack[2], -1, 0.1) # game over music
				pygame.display.update()

# Fireballs a player can shoot by using mana
class FireBall(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.direction = player.direction
		if self.direction == "RIGHT":
			self.image = load_image('fireball1_R.png')
		else:
			self.image = load_image('fireball1_L.png')
		# center the image around the player and add an offset to make sure that it appears from the center of the player
		self.rect = self.image.get_rect(center=player.pos)
		self.rect.x = player.pos.x
		self.rect.y = player.pos.y - 40
	
	def fire(self):
		player.magic_cooldown = True
		# Runs the animation while the fireball is still within the screen
		if -10 < self.rect.x < 710:
			if self.direction == "RIGHT":
				self.image = load_image('fireball1_R.png')
			else:
				self.image = load_image('fireball1_L.png')
			displaysurface.blit(self.image, self.rect)

			if self.direction == "RIGHT":
				self.rect.move_ip(12, 0) # move in place
			else:
				self.rect.move_ip(-12, 0)	
		else:
			self.kill()
			player.magic_cooldown = False
			player.attacking = False

class Bolt(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		super().__init__()
		self.image = load_image('bolt.png')
		self.rect = self.image.get_rect()
		self.rect.x = x + 15
		self.rect.y = y + 20
		self.direction = direction
	
	def fire(self):
		# Runs while the bolt is still within the screen
		if -10 < self.rect.x < 710:
			if self.direction == 0:
				self.image = load_image('bolt.png')
				displaysurface.blit(self.image, self.rect)
			else:
				self.image = load_image('bolt.png')
				displaysurface.blit(self.image, self.rect)
		
			if self.direction == 0:
				self.rect.move_ip(12, 0)
			else:
				self.rect.move_ip(-12, 0)
		
		else:
			self.kill()

		# Check for collision with player
		hits = pygame.sprite.spritecollide(self, player_group, False)
		if hits:
			player.player_hit()
			self.kill()
	
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = load_image('Enemy.png')
		self.rect = self.image.get_rect()
		self.pos = vec(0, 0)
		self.vel = vec(0, 0)
		self.direction = random.randint(0, 1) # 0 for Right direction, 1 for Left
		self.vel.x = random.randint(2, 6) / 2 # randomized velocity of the enemy
		self.mana_to_release = random.randint(1, 3) # randomized mana obtained from enemy after defeating it
		# Set the initial enemy position
		if self.direction == 0:
			self.pos.x = 0
			self.pos.y = 235
		if self.direction == 1:
			self.pos.x = 700
			self.pos.y = 235

	def move(self):
		if cursor.wait == 1: # do nothing if we are in pause mode
			return
		# Change directions right before reaching the edge of the screen
		if self.pos.x > (WIDTH - 20):
			self.direction = 1
		elif self.pos.x < 0:
			self.direction = 0

		# Move the enemy in the direction it is facing by subtracting or adding velocity to the position x value
		if self.direction == 0:
			self.pos.x += self.vel.x
		if self.direction == 1:
			self.pos.x -= self.vel.x

		# Update rect pos
		self.rect.center = self.pos
	
	def update(self):
		# Check for collision with the Player
		hits = pygame.sprite.spritecollide(self, player_group, False)
	
		# Check for collisions with fireballs
		f_hits = pygame.sprite.spritecollide(self, fireballs, False)
		
		# Activates upon either of the conditions being true
		if hits and player.attacking is True or f_hits:
			if player.mana < 100:
				player.mana += self.mana_to_release # release mana
			player.experience += 1 # release experience to player

			# Release item
			rand_num = np.random.uniform(0, 100) # uniform method ensures that there is no uneven spread of generated numbers
			item_type = 0
			if rand_num >= 0 and rand_num <= 5: # 6% chance of getting a heart
				item_type = 1
			elif rand_num > 5 and rand_num <= 15: # 10% chance of getting a coin
				item_type = 2
		
			# Add to item group
			if item_type != 0:
				item = Item(item_type)
				items.add(item)
				# Set the item position to the enemy position
				item.posx = self.pos.x
				item.posy = self.pos.y

			# Kill the enemy
			self.kill()
			print("Enemy killed")
			handler.dead_enemy_count += 1
			music_manager.playsound(hit, 0.15)

		# If collision has ocurred and player not attacking, the player has been hit
		elif hits and player.attacking is False:
			player.player_hit()

	def render(self):
		# Display an enemy on the screen
		displaysurface.blit(self.image, (self.pos.x, self.pos.y))

class RangedEnemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.pos = vec(0, 0)
		self.vel = vec(0, 0)
		
		self.direction = random.randint(0, 1) # 0 for Right direction, 1 for Left
		self.vel.x = random.randint(2, 6) / 3 # randomized velocity of the enemy
		self.mana_to_release = random.randint(2, 3) # randomized mana obtained from enemy after defeating it
		self.wait = 0
		self.wait_status = False
		self.turning = False # when the enemy should turn around

		if self.direction == 0:
			self.image = load_image('enemy2_R.png')
		if self.direction == 1:
			self.image = load_image('enemy2_L.png')
		self.rect = self.image.get_rect()
		
		# Set the initial enemy position
		if self.direction == 0:
			self.pos.x = 0
			self.pos.y = 250
		
		if self.direction == 1:
			self.pos.x = 700
			self.pos.y = 250
	
	def move(self):
		if cursor.wait == 1: # do nothing if we are in pause mode
			return
		# If the enemy is turning, call the turn method
		if self.turning is True:
			self.turn()
			return

		# Change directions right before reaching the edge of the screen
		if self.pos.x > (WIDTH - 20):
			self.direction = 1
		elif self.pos.x < 0:
			self.direction = 0

		# The ranged enemy moves a bit, pauses, attacks, and then moves again
		if int(self.wait) > 60:
			self.wait_status = True
		elif int(self.wait) <= 0:
			self.wait_status = False

		# Check if we need to turn around
		if(self.direction_check()):
			self.turn()
			self.wait = 90 # ensures the enemy waits a bit before turning, otherwise it looks weird to turn immediately
			self.turning = True

		# Enemy is in waiting state and can fire a bolt
		if self.wait_status is True:
			rand_num = np.random.uniform(0, 60)
			if int(rand_num) == 30:
				bolt = Bolt(self.pos.x, self.pos.y, self.direction)
				bolts.add(bolt)
			self.wait -= 1

		# If the enemy is not in waiting status, move the enemy in the direction it is facing by subtracting or adding velocity to the position x value
		elif self.direction == 0:
			self.pos.x += self.vel.x
			self.wait += self.vel.x
		elif self.direction == 1:
			self.pos.x -= self.vel.x
			self.wait -= self.vel.x

		# Update rect pos
		self.rect.topleft = self.pos
	
	def update(self):
		# Check for collision with the Player
		hits = pygame.sprite.spritecollide(self, player_group, False)
	
		# Check for collisions with fireballs
		f_hits = pygame.sprite.spritecollide(self, fireballs, False)
		
		# Activates upon either of the conditions being true
		if hits and player.attacking is True or f_hits:
			if player.mana < 100:
				player.mana += self.mana_to_release # release mana
			player.experience += 1 # release experience to player

			# Release item
			rand_num = np.random.uniform(0, 100) # uniform method ensures that there is no uneven spread of generated numbers
			item_type = 0
			if rand_num >= 0 and rand_num <= 5: # 6% chance of getting a heart
				item_type = 1
			elif rand_num > 5 and rand_num <= 15: # 10% chance of getting a coin
				item_type = 2
		
			# Add to item group
			if item_type != 0:
				item = Item(item_type)
				items.add(item)
				# Set the item position to the enemy position
				item.posx = self.pos.x
				item.posy = self.pos.y

			# Kill the enemy
			self.kill()
			print("Enemy killed")
			handler.dead_enemy_count += 1

	def direction_check(self):
		# player is behind the enemy and enemy pointing forwards
		if (player.pos.x - self.pos.x < 0 and self.direction == 0):
			return 1
		# player is in front of the enemy and enemy pointing backwards
		if (player.pos.x - self.pos.x > 0 and self.direction == 1):
			return 1
		else:
			return 0

	def turn(self):
		if self.wait > 0:
			self.wait -= 1
			return
		elif int(self.wait) <= 0:
			self.turning = False

		if self.direction:
			self.direction = 0
			self.image = load_image('enemy2_R.png')
		else:
			self.direction = 1
			self.image = load_image('enemy2_L.png')

	def render(self):
		# Display an enemy on the screen
		displaysurface.blit(self.image, self.rect)

class Castle(pygame.sprite.Sprite):
		def __init__(self):
			super().__init__()
			self.hide = False
			self.image = load_image('Castle.png')

		def update(self):
			if self.hide is False:
				displaysurface.blit(self.image, (400, 80))

class Item(pygame.sprite.Sprite):
	def __init__(self, item_type):
		super().__init__()
		# not fan of this design (one class for all items), but it's a start
		if item_type == 1:
			self.image = load_image('heart.png')
		elif item_type == 2:
			self.image = load_image('coin.png')
		self.rect = self.image.get_rect()
		self.type = item_type # to keep track for future use
		self.posx = 0
		self.posy = 0
		
	def render(self):
		self.rect.x = self.posx
		self.rect.y = self.posy
		displaysurface.blit(self.image, self.rect)

	def update(self):
		hits = pygame.sprite.spritecollide(self, player_group, False)
		# if item comes in contact with Player
		if hits:
			if player.health < 5 and self.type == 1:
				player.health += 1
				health.image = health_ani[player.health]
				self.kill()
			if self.type == 2:
				# add money to player
				self.kill()

class EventHandler():
	def __init__(self):
		self.enemy_count = 0
		self.dead_enemy_count = 0
		self.battle = False
		self.stage = 1
		# Enemy generation
		self.enemy_generation = pygame.USEREVENT + 2
		self.enemy_generation2 = pygame.USEREVENT + 3 # to generate enemies in a different world
		self.world = 0 # to keep track of which world we're in
		self.stage_enemies = []
		# a formula to calculate the number of enemies generated per level
		for x in range(1, 21):
			self.stage_enemies.append(int(( x ** 2 / 2) + 1))

	def stage_handler(self):
		# Code for the stage selection window
		self.root = Tk()
		self.root.geometry("200x170")

		button1 = Button(self.root, text = "Twilight Dungeon", width=18, height=2, command=self.world1)
		button2 = Button(self.root, text = "Skyward Dungeon", width=18, height=2, command=self.world2)
		button3 = Button(self.root, text = "Hell Dungeon", width=18, height=2, command=self.world3)

		button1.place(x=40,y=15)
		button2.place(x=40,y=65)
		button3.place(x=40,y=115)

		self.root.mainloop()

	def world1(self):
		self.root.destroy()
		button.img_display = 1 # change the button to a play/pause button
		pygame.time.set_timer(self.enemy_generation, 2000)
		castle.hide = True
		self.battle = True
		music_manager.playsoundtrack(soundtrack[1], -1, 0.05)
	
	def world2(self):
		self.root.destroy()
		background.bgimage = load_image('desert.jpg')
		ground.image = load_image('desert_ground.png')

		pygame.time.set_timer(self.enemy_generation2, 2500)
	
		self.world = 2
		button.img_display = 1 # change the button to a play/pause button
		castle.hide = True
		self.battle = True
		music_manager.playsoundtrack(soundtrack[1], -1, 0.05)

	def world3(self):
		self.battle = True
		button.img_display = 1 # change the button to a play/pause button
		music_manager.playsoundtrack(soundtrack[1], -1, 0.05)
  	# Empty for now

	# Code for when the next stage (ie: level) is clicked
	def next_stage(self):
		button.img_display = 1 # change the button to a play/pause button
		self.stage += 1

		self.enemy_count = 0
		self.dead_enemy_count = 0
		print("Stage: " + str(self.stage))

		if self.world == 1:
			pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage)) # increase the enemy generation speed per stage
		if self.world == 2:	
			pygame.time.set_timer(self.enemy_generation2, 1500 - (50 * self.stage)) # increase the enemy generation speed per stage

	def update(self):
		# Check if all enemies have been defeated in order to clear the stage
		if self.dead_enemy_count == self.stage_enemies[self.stage - 1]:
			self.dead_enemy_count = 0
			stage_display.cleared = True
			stage_display.stage_clear()
	
	def home(self):
		# reset battle code
		pygame.time.set_timer(handler.enemy_generation, 0)
		pygame.time.set_timer(handler.enemy_generation2, 0)

		self.battle = False
		self.enemy_count = 0
		self.dead_enemy_count = 0
		self.stage = 1
		self.world = 0
	
		# destroy any enemies or items lying around
		for group in enemies, items:
			for entity in group:
				entity.kill()
		
		# bring back backgrounds
		castle.hide = False
		background.bgimage = load_image('Background.png')
		ground.image = load_image('Ground.png')
		music_manager.playsoundtrack(soundtrack[0], -1, 0.05) # reset soundtrack
	
# Instantiate classes
background = Background()
ground = Ground()
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
enemies = pygame.sprite.Group()
items = pygame.sprite.Group()
fireballs = pygame.sprite.Group()
bolts = pygame.sprite.Group()
castle = Castle()
handler = EventHandler()
stage_display = StageDisplay()
health = HealthBar()
status_bar = StatusBar()
cursor = Cursor()
button = PButton()

# Sprite groups
ground_group = pygame.sprite.Group()
ground_group.add(ground)

# loading the soundtrack
music_manager = MusicManager()
music_manager.playsoundtrack(soundtrack[0], -1, 0.1)

# Game loop
while 1:
	player.gravity_check() # first check if the player is on the ground
	mouse = pygame.mouse.get_pos() # get the mouse position

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		# left click
		if event.type == MOUSEBUTTONDOWN:
			if 620 < mouse[0] <= 670 and 300 < mouse[1] <= 345:
				# Pause
				if button.img_display == 1:
					cursor.pause()
				# Home
				elif button.img_display == 0:
					handler.home()

		# Escape key to quit, just for convenience
		if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN and cursor.wait == 0: # only allow key presses if the game is not paused
			# Interact with the stage handler
			if event.key == pygame.K_e and 450 < player.rect.x < 550:
				handler.stage_handler()

			# Activate the next stage if no enemies are left
			if event.key == pygame.K_n:
				if handler.battle is True and len(enemies) == 0:
					handler.next_stage()
					stage_display.display = True
			
			# Fireball attack
			if event.key == pygame.K_f and player.magic_cooldown is False:
				if player.mana >= 6:
					player.mana -=6
					player.attacking = True
					fireball = FireBall()
					fireballs.add(fireball)
					music_manager.playsound(fsound, 0.3)

			if event.key == pygame.K_SPACE:
				player.jump()
		
			if event.key == pygame.K_RETURN:
				if player.attacking is False:
					player.attacking = True # trigger the attack animation
		
		if event.type == hit_cooldown:
			# once cooldown period has passed, disable cooldown and stop the timer so it doesn't trigger again
			player.cooldown = False
			pygame.time.set_timer(hit_cooldown, 0)

		if event.type == handler.enemy_generation:
			# Keep adding enemies until you reach the max number of enemies per stage
			if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
				enemy = Enemy()
				enemies.add(enemy)
				handler.enemy_count += 1
		
		if event.type == handler.enemy_generation2:
			# Keep adding enemies until you reach the max number of enemies per stage
			if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
				if handler.enemy_count % 2: # alternate between
					enemy = RangedEnemy()
				else:
					enemy = Enemy()
				enemies.add(enemy)
				handler.enemy_count += 1
	
	# Render background and display
	background.render()
	ground.render()
	# Render button and cursor
	button.render(button.img_display)
	cursor.hover()
	
	# Render Sprites
	castle.update()
	if player.health > 0:
		displaysurface.blit(player.image, player.rect)
	
	# Status, health, and stage updates
	health.render()
	displaysurface.blit(status_bar.surf, (580, 5))
	status_bar.update_draw()
	handler.update()

	# Update and render sprites
	player.update()
	if player.attacking is True:
		player.attack() # ensure the attack animation plays until the frames have been executed
	player.move()
	for ball in fireballs:
			ball.fire()
	for bolt in bolts:
		bolt.fire()     
	for entity in enemies:
		entity.update()
		entity.move()
		entity.render()
	for item in items:
		item.render()
		item.update()
	
	# Update and render the stage displays
	if stage_display.display is True:
		stage_display.move_display()
	if stage_display.cleared is True:
		stage_display.stage_clear()

	pygame.display.update()
	FPS_CLOCK.tick(FPS)
