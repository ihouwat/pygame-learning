import pygame
from pygame.locals import *
import sys
import random
from tkinter import * # Tkinter is a GUI library that comes with Python
from tkinter import filedialog
import os
import pathlib

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

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG") # Window title

# util method to load images
def load_image(fileName) -> pygame.Surface:
	file_path = os.path.join(os.path.dirname(pathlib.Path(__file__).absolute()), 'images', fileName)
	return pygame.image.load(file_path)

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

# Custom events
hit_cooldown = pygame.USEREVENT + 1 # create a unique event we will use to implement an 'invulnerability' period after being hit by an enemy, so the player doesn't lose all their health in one frame

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

class StageDisplay(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.text = heading_font.render("Stage: " + str(handler.stage), True, color_dark)
		self.rect = self.text.get_rect()
		self.posx = -100 # initialize off screen
		self.posy = 100
		self.diplay = False

	def move_display(self):
		# Create the text to be displayed
		self.text = heading_font.render("STAGE: " + str(handler.stage) , True , color_dark)
		if self.posx < 700:
			self.posx += 5
			displaysurface.blit(self.text, (self.posx, self.posy))
		else:
			self.display = False
			self.kill()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = load_image('Player_Sprite_R.png')
		self.rect = self.image.get_rect()
		self.health = 5
	
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
		# If attack frame has reached end of sequence, return to base frame and end the attack
		if self.attack_frame > 10:
			self.attack_frame = 0
			self.attacking = False

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
			print("Player was hit")

			if self.health == 0:
				print("Player died")
				self.kill()
				pygame.display.update()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = load_image('Enemy.png')
		self.rect = self.image.get_rect()
		self.pos = vec(0, 0)
		self.vel = vec(0, 0)
		self.direction = random.randint(0, 1) # 0 for Right direction, 1 for Left
		self.vel.x = random.randint(2, 6) # randomized velocity of the enemy
		# Set the initial enemy position
		if self.direction == 0:
			self.pos.x = 0
			self.pos.y = 235
		if self.direction == 1:
			self.pos.x = 700
			self.pos.y = 235

	def move(self):
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
		
		# Activates upon either of the conditions being true
		if hits and player.attacking is True:
			self.kill()
			print("Enemy killed")

		# If collision has ocurred and player not attacking, the player has been hit
		elif hits and player.attacking is False:
			player.player_hit()

	def render(self):
		# Display an enemy on the screen
		displaysurface.blit(self.image, (self.pos.x, self.pos.y))

class Castle(pygame.sprite.Sprite):
		def __init__(self):
			super().__init__()
			self.hide = False
			self.image = load_image('Castle.png')

		def update(self):
			if self.hide is False:
				displaysurface.blit(self.image, (400, 80))

class EventHandler():
	def __init__(self):
		self.enemy_count = 0
		self.battle = False
		self.stage = 1
		# Enemy generation
		self.enemy_generation = pygame.USEREVENT + 2
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
		pygame.time.set_timer(self.enemy_generation, 2000)
		castle.hide = True
		self.battle = True
	
	def world2(self):
		self.battle = True
		# Empty for now
	
	def world3(self):
		self.battle = True
		# Empty for now

	# Code for when the next stage (ie: level) is clicked
	def next_stage(self):
		self.stage += 1
		self.enemy_count = 0
		print("Stage: " + str(self.stage))
		pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage)) # increase the enemy generation speed per stage

# Instantiate classes
background = Background()
ground = Ground()
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
enemies = pygame.sprite.Group()
castle = Castle()
handler = EventHandler()
stage_display = StageDisplay()
health = HealthBar()

# Sprite groups
ground_group = pygame.sprite.Group()
ground_group.add(ground)

# Game loop
while True:
	player.gravity_check() # first check if the player is on the ground

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		# left click
		if event.type == MOUSEBUTTONDOWN: 
			pass

		if event.type == KEYDOWN:
			# Interact with the stage handler
			if event.key == pygame.K_e and 450 < player.rect.x < 550:
				handler.stage_handler()

			# Activate the next stage if no enemies are left
			if event.key == pygame.K_n:
				if handler.battle is True and len(enemies) == 0:
					handler.next_stage()
					stage_display = StageDisplay()
					stage_display.diplay = True

			if event.key == pygame.K_SPACE:
				player.jump()
		
			if event.key == pygame.K_RETURN:
				if player.attacking is False:
					player.attacking = True # trigger the attack animation

			# Escape key to quit, just for convenience
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		
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
	
	# Render background and display
	background.render()
	ground.render()
	
	# Render Sprites
	castle.update()
	if player.health > 0:
		displaysurface.blit(player.image, player.rect)
	health.render()

	# Update Sprites
	player.update()
	if player.attacking is True:
		player.attack() # ensure the attack animation plays until the frames have been executed
	player.move()
	for entity in enemies:
		entity.update()
		entity.move()
		entity.render()
	if stage_display.display is True:
		stage_display.move_display()

	pygame.display.update()
	FPS_CLOCK.tick(FPS)
