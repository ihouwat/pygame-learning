
# Starting ideas
- SCRATCH THAT IDEA -do we need the timer/rotate options level?? seems to much for a toddler
- DONE need an Item class with these properties: image, sound, word, text_identifier
- DONE need dictionary to load images and sounds during the game (don't load images in classes!) - toggle language thru some enum
- with the item dataclass, do we pass the image and sound as a path or as a resource???

# Todo
- DONE create a dictionary of items and a dataclass for the items
	- why a dataclass --> it is just for data and makes comparing items easier
- DONE add one item to the game to test dataclass approach
- DONE try one round of the game with only 4 items
- DONE try one round of the game with 4 randomly picked items
- DONE add one more level to the game to see what we need to manage multiple levels
- DONE tidying up stage
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
- DONE tidying up stage: move classes into separate files
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
- DONE configure logging
- DONE add animations
	- DONE increase sprite size on hover, decrease on mouse out
	- DONE fade sprites in/out between puzzles
	- DONE new level animation
- DONE tidying up stage:
	- DONE `ItemSprite` class:
		- DONE the scaling function for shapes is buggy. i *think* it's because at some point the scaling factor is larger than the image size
		- DONE clean up some of the properties now we have the metadata. perhaps combine word and text_identifier properties?
	- DONE Transitions in `Game` class:
		- DONE destroy sprites when you end the turn, that allows you to split the sprite destruction from creation 
		- DONE ??? Instead of animating the sprites in both the start and end states, create a transition state to manage animations? But that is exactly what the start state does...
	- DONE Refactor the for loops that scale multiple sprites in the `Game` class. 
	- DONE add `AudioPlayer` class with dummy implementations to test the code structure
	- DONE Where to put those scaling animations? `SpriteHandler` or somewhere else? Answer is `AnimationEngine` that consumes`Animation` objects and executes them.
	- DONE Split game states using state machine pattern
	- DONE Split sprite scaling animation such that it handles one sprite and then add different sprites to the animations list
	- DONE Have animations return true if they have completed over a number of game loop turns.
		- DONE This requires that we have class vars for sprites and text (also add Text class)
	- DONE Create TextElement class to create text objects
		- DONE use those for level transitions from game class
		- replace the text elements in the status bar with TextElement objects
	- DONE Fix the rest of the animations (turn ending fade out, level ending, etc.)
	- DECISION: DON'T DO IT - Create a `GameState` or `GameContext` data class to pass game data around or reuse `Game` class???
		- Advantage of data class means we pass only the context we need, as opposed to the entire game instance --> better encapsulation
		- Disadvantage is coupling and we might be breaking encapsulation by passing too much `Game` data around
- DONE add a game completed screen
- DONE download more pngs
	- DONE add vehicles category
- DONE Sounds
	- DONE add music
		- DONE add intro music
		- DONE add background music
		- DONE victory music and attribution
	- DONE add sound effects
		- DONE on success
			- DONE load a 'ding' sound effect
			- DONE load a 'clap' sound effect between levels
			- DONE load and play the sound in the target language and a sound effect: loading dynamically allows us to switch languages mid-game without resetting the sprites
		- DONE on failure, play some 'try again' sound
	- DONE record and add languages to the game
		- DONE English
		- DONE Arabic
		- DONE Portuguese
		- DONE need to add a language dict to toggle languages
		- DONE refactor audioplayer to load spoken words and cache
		- DONE configure volume settings so we can hear voice over the music
		- DONE create a shapes config where the sound is the color of the shape, and apply it to the appropriate puzzle.
- DONE tidying up:
	- DONE name change from ProcessPointResult to something appropriate
	- DONE Bug fixes
		- DONE Last level plays only one puzzle (`level_up()` method is called too early)
		- DONE images transition in and then scale down abruptly at the beginning of each turn (the screen not wide enough??)
	- DONE `Game` class:
		- DONE has two methods that animate text, one when we win a level, and one where we win the game. Combine them.
		- DONE a bunch of animations in there, should i split them out?
		- DONE there is a mention of a 'default.wav' file in the code. that is a temp placeholder when loading a spoken word. need better handling of that.
		- DONE Move the mouse selection of correct sprites to event listener, that way the returned game action indicates the the right answer is selected
	- DONE `Renderer` class:
		- DONE (NOT NEEDED) - checks two game states to render text, one for completing a level, the other for completing a game. Can we combine them?
		- DONE the game completed animation is a nested conditional. Let's clean that up.
	- DONE Tidying:
		- DONE move constants, enums, and classes closer to where they are used. For example, there is a SoundTrack type that can be moved to the audio folder. There is a SoundEffect class that can be moved to the audio folder. Etc etc etc
		- DONE Instantiate GameState classes once, and instead of them having instance variables, just pass in the game instance and GameContext each time you invoke the execute() function

- text in status bar
- DONE clean up sprite handler dead code
- consider 'fancy' animations for transitions
	- DONE transition delays at the end of the scale up/scale down animations
	- **cascade animate the sprites** (ie each sprite in a group starts getting animated but delayed by a few frames): **The problem is that we have to manage the sprite animations for every frame**. So, in addition to having `Animation` classes, which execute the animations per sprite per frame, we need a `Transition` class or function that tracks a group sprites over the animation lifecycle. To implement the cascade delay
		- a quick way is to track the sprite scales, set some scale threshold after which the next sprite can be animated, and use that calculation to determine which sprites should be animated at each frame.
		- A better way is to store the starting frame at which the animations begin and then delay the animation start for each sprite by a few frames. We'd need some way to `start()` and detect when the group animation `is_completed()`. This second approach is a bit more complicated as we need to store an initial frame and track frame numbers over multiple game loops.

- update readme with what i did and my learnings (PyGame, basic game design, practicing Python OOP, working with Copilot, you have to think at the level of each frame, which gets tricky the moment the animations or game states get slightly complicated (ex: staggered animations, transitions between turns/levels))

## Learnings
### State machine pattern
A state machine, also known as a finite state machine (FSM), is a model of computation or behavior composed of a finite number of states, transitions between those states, and actions. It's a mathematical model of computation, an abstract concept where the machine can have different states but at a given time fulfills only one of them.

In the context of programming and software development, state machines are used to model the behavior of an object, which can be in a finite number of states and can transition from one state to another based on certain conditions.
- The state machine pattern is a behavioral design pattern that allows an object to change its behavior when its internal state changes. This pattern is used when a system has a finite number of states and can transition from one state to another based on certain conditions.

In the context of a game, the state machine pattern can be used to manage game states, such as `PLAYING`, `PAUSED`, `MENU_OPEN`, etc. The game can only be in one state at a time, and transitions between states are triggered by certain events or conditions, such as user input or game logic.
