# PyGame Tutorial - Game Engine
source: http://pygametutorials.wikidot.com/tutorials-basic

## PyGame
PyGame can handle time, video (both still images and vids), music, fonts, different image formats, cursors, mouse, keyboard, Joysticks and much much more. And all of that is very simple.

## Game Loop
Game loop is the place where events, game logic and rendering onto the screen is performed.
It should look similar to:

```
while True:
	events()
	loop()
	render()
```

* event() proceeds events like pressed keys, mouse motion etc.
* loop() compute changes in the game world like NPC's moves, player moves, AI, game score. 
* *render() just print out on the screen graphic. 

That separation of tasks makes your game design easier and allow for easy changes in code

## Notes
* OOP is popupar in PyGame due to the fact that it is easy to create classes for game objects like player, enemy, bullet etc.
* App is the main class. To run a game, we call the on_execute() function, which contains a game loop.

## Reading
* [magic methods](https://rszalski.github.io/magicmethods/#:~:text=What%20are%20magic%20methods%3F,as%20they%20need%20to%20be.)
* ["__name__"](https://towardsdatascience.com/python-main-b729fab7a8c3#:~:text=Before%20executing%20a%20program%2C%20the,__name__%20will%20vary.)
* ["__main__" and Top-level code environment](https://docs.python.org/3/library/__main__.html#:~:text=__main__%20is%20the,entry%20point%20to%20the%20application.)
	* When a Python module or package is imported, __name__ is set to the module’s name. Usually, this is the name of the Python file itself without the .py extension
	* However, if the module is executed in the top-level code environment, its __name__ is set to the string '__main__'.
	* “Top-level code” is the first user-specified Python module that starts running. It’s “top-level” because it imports all other modules that the program needs. Sometimes “top-level code” is called an entry point to the application. Examples:
		*  the scope of an interactive prompt ```>>> __name__```
		* a module passed to the interpreter as a file argument ```python helloworld.py```