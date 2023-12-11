
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

- refactor the classes and cleanup code
	- maybe have a dataclass for the pure data that you can inject into another class for the sprite representation?
	- DONE need class for rendering
	- need class for puzzles, etc.
	- need to decouple rendering from the game logic??
	- perhaps need a class for user event handling...

- download more pngs and add attributions
- create more levels (colored shapes, items, grayscale items, voice only target item)
- add the menu
- add languages

Game states
* Menu: the menu screen
* Game: the game screen
* Pause: the game is paused
* Game Over: the game is over (nah we don't want that with a kiddo :) )

