import random

import pygame
from config.game_items import GameItemConfig
from config.interfaces import SpriteOption
from funcs import load_pygame_image
from game_objects.models.item import Item
from pygame.sprite import Group, Sprite


class SpriteHandler:
	""" Handles the creation of sprites and sprite groups. """
	
	@staticmethod
	def create_sprite_group(max_number: int, items: list[GameItemConfig], option: SpriteOption = None) -> Group:
		""" Creates a sprite group given a list of items."""
		narrowed_down_items: list = SpriteHandler.pick_items_from_list(items, max_number)
		sprite_group: Group = SpriteHandler.create_group(narrowed_down_items, option)
		return sprite_group

	@staticmethod
	def create_group(items: list[GameItemConfig], option: SpriteOption) -> Group:
		""" Creates a sprite group out of a list of items.
		
		Args:
			items (list[GameItemConfig]): A list of gmae items to be used to create the sprite group.
			option (Option): An option to be applied to the sprite.
		"""
		group = pygame.sprite.Group()
		for item in items:
			group.add(Item(
			image=SpriteHandler.retrieve_image(item.image, option),
			text_identifier=item.text_identifier,
			word=item.word
		))

		return group

	@staticmethod
	def retrieve_image(image: str | pygame.Surface, option: SpriteOption) -> pygame.Surface:
		""" Retrieves the image for a sprite based on an option."""
		if option == SpriteOption.SHAPES:
			src_image = image # shapes images are created as surfaces
		# if option == SpriteOption.SPOKENWORD:
		# 	# TODO Change to use the 'sound' image
		# 	src_image = load_pygame_image('assets', 'images', image)
		else:
			src_image = load_pygame_image('assets', 'images', image)
			print(src_image)
			if option == SpriteOption.GRAYSCALE:
				src_image=pygame.transform.grayscale(src_image)

		return src_image
	
	@staticmethod
	def pick_items_from_list(list_of_items: list, max_number: int) -> list:
		""" Picks a random number of items from a list of game items. 
		
		Args:
			list_of_items (list): A list of items to pick from.
			max_number (int): The maximum number of items to pick.
		"""
		used_indexes = set()
		items = []

		while len(items) < max_number:
			item_index = random.randint(0, len(list_of_items) - 1)
			if item_index not in used_indexes:
				used_indexes.add(item_index)
				items.append(list_of_items[item_index])
			else:
				continue

		return items

	@staticmethod
	def pick_item_to_match(items: Group) -> Sprite:
		""" Picks a random item from a sprite group."""
		return random.choice(items.sprites())
	
	@staticmethod
	def kill_sprite_group(group: Group) -> None:
		""" Removes all sprites from a sprite group."""
		for sprite in group:
			sprite.kill()
	
	@staticmethod
	def kill_sprite(sprite: Sprite) -> None:
		""" Removes a sprite from a sprite group."""
		sprite.kill()
