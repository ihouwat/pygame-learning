
Ideas:
- SCRATCH THAT IDEA -do we need the timer/rotate options level?? seems to much for a toddler
- DONE need an Item class with these properties: image, sound, word, text_identifier
- DONE need dictionary to load images and sounds during the game (don't load images in classes!) - toggle language thru some enum
- with the item dataclass, do we pass the image and sound as a path or as a resource???

Progress:
- DONE create a dictionary of items and a dataclass for the items
	- why a dataclass --> it is just for data and makes comparing items easier
- DONE add one item to the game to test dataclass approach
- DONE try one round of the game with only 4 items
- DONE try one round of the game with 4 randomly picked items
- DONE add one more level to the game to see what we need to manage multiple levels
- DONE refactor the classes and cleanup code
	- maybe have a dataclass for the pure data that you can inject into another class for the sprite representation?
	- DONE need class for rendering
	- DONE need class for puzzles, etc.
	- NOT NEEDED: need to decouple rendering from the game logic?? (rendering logic is simple enough)
	- DONE perhaps need a class for user event handling...
- DONE generate docstrings

- create more levels
	- DONE many shapes with one color
	- DONE many shapes with many colors
	- DONE one shape with many colors
	- DONE many types of colored items (ex: fruits, vehicles, animals, etc.)
	- DONE grayscale items
	- DONE one type of colored items (ex: only fruits)
	
- PARTIALLY DONE voice only target item (need to still record sounds)

- DONE refactor by moving classes into separate files
	- DONE Created config, engine, game_objects files
	- DONE Need to find a home from game_manager
	- DONE Need to find a home for the funcs.py
	- DONE Need to move setup logic out of main.py into game_setup.py
	- DONE Need to reexamine config folder
- DONE add status bar
- DONE add the menu
	- DONE Play action
	- DONE quit action
	- DONE enter name
	- DONE choose language

- add animations
	- fade sprites in/out???
	- level number animation
	- increase sprite size on hover

- download more pngs and add attributions
- record and add languages
- add music

Game states
* Menu: the menu screen
* Game: the game screen
* Pause: the game is paused (no need, we will not be using a timer)
* Game Over: the game is over (nah we don't want that with a kiddo :) )

