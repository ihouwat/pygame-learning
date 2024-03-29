import random

import pygame
from config.logger import logger
from game_objects.item_sprite import ItemSprite
from models.game_types import SpriteOption
from models.image_source import ImageSource
from models.item_config import ItemConfig
from pygame.sprite import Group, Sprite


class SpriteHandler:
	""" Handles the creation of sprites and sprite groups. """
	
	@staticmethod
	def create_sprite_group(max_number: int, item_configs: list[ItemConfig], option: SpriteOption) -> Group:
		""" Creates a sprite group given a list of items."""
		narrowed_down_items: list[ItemConfig] = SpriteHandler.pick_items_from_list(item_configs, max_number)
		sprite_group: Group = SpriteHandler.create_group(narrowed_down_items, option)
		return sprite_group

	@staticmethod
	def create_group(item_configs: list[ItemConfig], option: SpriteOption) -> Group:
		""" Creates a sprite group out of a list of items.
		
		Args:
			items (list[ItemConfig]): A list of gmae items to be used to create the sprite group.
			option (Option): An option to be applied to the sprite.
		"""
		group = pygame.sprite.OrderedUpdates() # draws Sprites in order of addition 
		for item in item_configs:
			group.add(ItemSprite(
			image=SpriteHandler.retrieve_image(item.image, option),
			text_identifier=item.text_identifier,
			metadata=item
		))

		return group

	@staticmethod
	def retrieve_image(image: ImageSource, option: SpriteOption) -> pygame.Surface:
		""" Retrieves the image for a sprite based on an option."""
		src_image = image.get_image()
		if option == SpriteOption.GRAYSCALE:
			src_image=pygame.transform.grayscale(src_image)

		return src_image

	@staticmethod
	def pick_items_from_list(list_of_items: list, max_number: int) -> list:
		""" Picks a random number of items from a list of game items. 
		
		Args:
			list_of_items (list): A list of items to pick from.
			max_number (int): The maximum number of items to pick.

		Raises:
			ValueError: If the list of items is empty.
		"""
		if not list_of_items:
			raise ValueError('list_of_items is empty')

		used_indexes = set()
		items = []
		counter = 0

		while len(items) < max_number:
			item_index = random.randint(0, len(list_of_items) - 1)
			if item_index not in used_indexes:
				used_indexes.add(item_index)
				items.append(list_of_items[item_index])
				counter += 1

			if counter == len(list_of_items):
				logger.warning('Ran out of items to pick from because the list. Resetting the list of used indexes.')
				used_indexes.clear()
				counter = 0

		return items

	@staticmethod
	def pick_item_to_match(items: Group) -> ItemSprite:
		""" Picks a random item from a sprite group and returns a copy."""
		return ItemSprite.create_from(sprite=random.choice(items.sprites()))
	
	@staticmethod
	def kill_sprite_group(group: Group) -> None:
		""" Removes all sprites from a sprite group."""
		for sprite in group:
			sprite.kill()
	
	@staticmethod
	def kill_sprite(sprite: Sprite) -> None:
		""" Removes a sprite from a sprite group."""
		sprite.kill()
