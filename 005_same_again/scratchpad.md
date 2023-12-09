
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
	- once done need to download more pngs and add attributions
extract the classes
	- maybe have a dataclass for the pure data as opposed to the sprite representations?
add one more round
add the menu
add languages

Game states
* Menu: the menu screen
* Game: the game screen
* Pause: the game is paused
* Game Over: the game is over (nah we don't want that with a kiddo :) )

