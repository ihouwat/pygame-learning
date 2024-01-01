from config.settings import colors
from funcs import create_shape
from models.game_types import (
    Color,
    ItemCategory,
    RealWorldObjectCategory,
    Shape,
)
from models.image_source import PathSource, SurfaceSource
from models.item_config import ItemConfig

""" Game items will be used to create sprites for the puzzles that will be used in the game. 
  There are two types of game items:
    1. Items: A sprite that represents an object from an image.
    2. Shapes: A sprite that represents a shape drawn with the Pygame API.
"""

# game_items: list[Item] = [Item(**x) for x in [
# 	{"text_identifier": "banana", "image": "img", "sound": "mp3", "word": "Banana"},
# 	{"text_identifier": "apple", "image": "img", "sound": "mp3", "word": "Apple"},
# 	{"text_identifier": "orange", "image": "img", "sound": "mp3", "word": "Orange"},
# 	{"text_identifier": "pear", "image": "img", "sound": "mp3", "word": "Pear"},
# 	{"text_identifier": "grapes", "image": "img", "sound": "mp3", "word": "Grapes"},
# 	{"text_identifier": "strawberry", "image": "img", "sound": "mp3", "word": "Strawberry"},
# 	{"text_identifier": "pineapple", "image": "img", "sound": "mp3", "word": "Pineapple"},
# 	{"text_identifier": "watermelon", "image": "img", "sound": "mp3", "word": "Watermelon"},

# 	{"text_identifier": "carrot", "image": "img", "sound": "mp3", "word": "A carrot"},
# 	{"text_identifier": "potato", "image": "img", "sound": "mp3", "word": "A potato"},
# 	{"text_identifier": "onion", "image": "img", "sound": "mp3", "word": "An onion"},
# 	{"text_identifier": "tomato", "image": "img", "sound": "mp3", "word": "A tomato"},
# 	{"text_identifier": "cucumber", "image": "img", "sound": "mp3", "word": "A cucumber"},
# 	{"text_identifier": "pepper", "image": "img", "sound": "mp3", "word": "A pepper"},
# 	{"text_identifier": "broccoli", "image": "img", "sound": "mp3", "word": "Broccoli"},
# 	{"text_identifier": "lettuce", "image": "img", "sound": "mp3", "word": "Lettuce"},
# 	{"text_identifier": "mushroom", "image": "img", "sound": "mp3", "word": "A mushroom"},
# 	{"text_identifier": "corn", "image": "img", "sound": "mp3", "word": "Corn"},


# 	{"text_identifier": "chair", "image": "img", "sound": "mp3", "word": "A chair"},
# 	{"text_identifier": "table", "image": "img", "sound": "mp3", "word": "A table"},
# 	{"text_identifier": "couch", "image": "img", "sound": "mp3", "word": "A couch"},
# 	{"text_identifier": "bed", "image": "img", "sound": "mp3", "word": "A bed"},
# 	{"text_identifier": "lamp", "image": "img", "sound": "mp3", "word": "A lamp"},
# 	{"text_identifier": "television", "image": "img", "sound": "mp3", "word": "A television"},
# 	{"text_identifier": "computer", "image": "img", "sound": "mp3", "word": "A computer"},
# 	{"text_identifier": "refrigerator", "image": "img", "sound": "mp3", "word": "A refrigerator"},
# 	{"text_identifier": "microwave", "image": "img", "sound": "mp3", "word": "A microwave"},
# 	{"text_identifier": "toaster", "image": "img", "sound": "mp3", "word": "A toaster"},

# 	{"text_identifier": "dog", "image": "img", "sound": "mp3", "word": "A dog"},
# 	{"text_identifier": "cat", "image": "img", "sound": "mp3", "word": "A cat"},
# 	{"text_identifier": "bird", "image": "img", "sound": "mp3", "word": "A bird"},
# 	{"text_identifier": "fish", "image": "img", "sound": "mp3", "word": "A fish"},
# 	{"text_identifier": "rabbit", "image": "img", "sound": "mp3", "word": "A rabbit"},
# 	{"text_identifier": "hamster", "image": "img", "sound": "mp3", "word": "A hamster"},
# 	{"text_identifier": "horse", "image": "img", "sound": "mp3", "word": "A horse"},
# 	{"text_identifier": "turtle", "image": "img", "sound": "mp3", "word": "A turtle"},
# 	{"text_identifier": "snake", "image": "img", "sound": "mp3", "word": "A snake"},
# 	{"text_identifier": "frog", "image": "img", "sound": "mp3", "word": "A frog"},
# ]]

items_config: list[ItemConfig] = [
  ItemConfig(**x)
  for x in [
    # Fruits
    {"text_identifier": "banana", "image": PathSource("banana.png"), "sound": "mp3", "word": "Banana", "color": Color.YELLOW, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "strawberry", "image": PathSource("strawberry.png"), "sound": "mp3", "word": "Strawberry", "color": Color.RED, "type":RealWorldObjectCategory.FRUIT},
    {"text_identifier": "pear", "image": PathSource("pear.png"), "sound": "mp3", "word": "Pear", "color": Color.RED, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "apple", "image": PathSource("apple.png"), "sound": "mp3", "word": "Apple", "color": Color.GREEN, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "pineapple", "image": PathSource("pineapple.png"), "sound": "mp3", "word": "Pineapple", "color": Color.YELLOW, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "orange", "image": PathSource("orange.png"), "sound": "mp3", "word": "Orange", "color": Color.ORANGE, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "watermelon", "image": PathSource("watermelon.png"), "sound": "mp3", "word": "Watermelon", "color": Color.GREEN, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "grapes", "image": PathSource("grapes.png"), "sound": "mp3", "word": "Grapes", "color": Color.PURPLE, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "peach", "image": PathSource("peach.png"), "sound": "mp3", "word": "Peach", "color": Color.ORANGE, "type": RealWorldObjectCategory.FRUIT},
    {"text_identifier": "cherry", "image": PathSource("cherry.png"), "sound": "mp3", "word": "Cherry", "color": Color.RED, "type": RealWorldObjectCategory.FRUIT},
    
    # Vegetables
    {"text_identifier": "eggplant", "image": PathSource("eggplant.png"), "sound": "mp3", "word": "Eggplant", "color": Color.PURPLE, "type": RealWorldObjectCategory.VEGETABLE},
    {"text_identifier": "tomato", "image": PathSource("tomato.png"), "sound": "mp3", "word": "Tomato", "color": Color.RED, "type": RealWorldObjectCategory.VEGETABLE},
    {"text_identifier": "sweet potato", "image": PathSource("sweet_potato.png"), "sound": "mp3", "word": "Sweet potato", "color": Color.ORANGE, "type": RealWorldObjectCategory.VEGETABLE},
    {"text_identifier": "mushroom", "image": PathSource("mushroom.png"), "sound": "mp3", "word": "Mushroom", "color": Color.WHITE, "type": RealWorldObjectCategory.VEGETABLE},
    
    # Animals
    {"text_identifier": "cat", "image": PathSource("cat.png"), "sound": "mp3", "word": "Cat", "color": Color.ORANGE, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "chicken", "image": PathSource("chicken.png"), "sound": "mp3", "word": "Chicken", "color": Color.WHITE, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "bear", "image": PathSource("bear.png"), "sound": "mp3", "word": "Bear", "color": Color.BROWN, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "rabbit", "image": PathSource("rabbit.png"), "sound": "mp3", "word": "Rabbit", "color": Color.WHITE, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "panda", "image": PathSource("panda.png"), "sound": "mp3", "word": "Panda", "color": Color.WHITE, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "pig", "image": PathSource("pig.png"), "sound": "mp3", "word": "Pig", "color": Color.PINK, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "mouse", "image": PathSource("mouse.png"), "sound": "mp3", "word": "Mouse", "color": Color.GREY, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "monkey", "image": PathSource("monkey.png"), "sound": "mp3", "word": "Monkey", "color": Color.BROWN, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "horse", "image": PathSource("horse.png"), "sound": "mp3", "word": "Horse", "color": Color.BROWN, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "koala", "image": PathSource("koala.png"), "sound": "mp3", "word": "Koala", "color": Color.GREY, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "frog", "image": PathSource("frog.png"), "sound": "mp3", "word": "Frog", "color": Color.GREEN, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "dog", "image": PathSource("dog.png"), "sound": "mp3", "word": "Dog", "color": Color.BROWN, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "cow", "image": PathSource("cow.png"), "sound": "mp3", "word": "Cow", "color": Color.WHITE, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "chick", "image": PathSource("chick.png"), "sound": "mp3", "word": "Chick", "color": Color.YELLOW, "type": RealWorldObjectCategory.ANIMAL},
    {"text_identifier": "tiger", "image": PathSource("tiger.png"), "sound": "mp3", "word": "Tiger", "color": Color.ORANGE, "type": RealWorldObjectCategory.ANIMAL},
    
    # Vehicles
    {"text_identifier": "ambulance", "image": PathSource("ambulance.png"), "sound": "mp3", "word": "Ambulance", "color": Color.WHITE, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "bicycle", "image": PathSource("bicycle.png"), "sound": "mp3", "word": "Bicycle", "color": Color.RED, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "bus", "image": PathSource("bus.png"), "sound": "mp3", "word": "Bus", "color": Color.ORANGE, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "car", "image": PathSource("car.png"), "sound": "mp3", "word": "Car", "color": Color.GREEN, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "helicopter", "image": PathSource("helicopter.png"), "sound": "mp3", "word": "Helicopter", "color": Color.BLUE, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "plane", "image": PathSource("plane.png"), "sound": "mp3", "word": "Plane", "color": Color.YELLOW, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "ship", "image": PathSource("ship.png"), "sound": "mp3", "word": "Ship", "color": Color.GREY, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "tractor", "image": PathSource("tractor.png"), "sound": "mp3", "word": "Tractor", "color": Color.RED, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "train", "image": PathSource("train.png"), "sound": "mp3", "word": "Train", "color": Color.BLUE, "type": RealWorldObjectCategory.VEHICLE},
    {"text_identifier": "truck", "image": PathSource("truck.png"), "sound": "mp3", "word": "Truck", "color": Color.GREY, "type": RealWorldObjectCategory.VEHICLE},

  ]
]

shapes_config: list[ItemConfig] = [
  ItemConfig(
        text_identifier=str(shape.value),
        image=SurfaceSource(create_shape(shape, color_value)),
        sound=str(shape.value),
        word=str(shape.value),
        color=color_name,
        type="Shape"
    )
  for shape in Shape
  for color_name, color_value in colors.items()
]

game_items_catalog: dict[ItemCategory, list[ItemConfig]] = {
  ItemCategory.REAL_WORLD_OBJECTS: items_config,
  ItemCategory.SHAPES: shapes_config
}
