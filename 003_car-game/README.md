# Python PyGame Tutorial – The Complete Guide
source: https://coderslegacy.com/python/python-pygame-tutorial/

## Introduction
The Pygame library is probably the most well known python library when it comes to making games. It’s not the most advanced or high level library, but it’s comparatively simple and easy to learn. Pygame serves as a great entry point into the world of graphics and game development, especially for beginners.

The Pygame framework includes several modules with functions for drawing graphics, playing sounds, handling mouse input, and other things that you’ll need while developing games in Python.

## Concepts

### Setting up a game

Imports the pygame library and all the functaionlity defined in the pygame.locals module.
```
import pygame
from pygame.locals import *
```
**The init() function in pygame initializes the pygame engine**. This line must be included before you begin writing any pygame code.
```python
pygame.init()
```

### The Game Loop
**The Game Loop is where all the game events occur, update, and get drawn to the screen**. Once the initial setup and initialization of variables is out of the way, the Game Loop begins where the program keeps looping over and over until an event of type `QUIT` occurs.

**A Game Loop is a simple `while` loop that runs indefinitely**. It looks like this:
```python
#Game loop begins
while True:
      # Code
      # More Code
      .
      .
      pygame.display.update()
```
Changes in the game are not implemented until the `pygame.display.update()` function has been called. This **function updates the game window** with any changes that have been made within that specific iteration of the game loop. 

The function **keeps our display screen updated with the latest changes** from every iteration. We place it at the very end so that all possible changes to the Sprites on the screen have already taken place.

#### Quitting the Game Loop
**Every game loop must have an end point**, or a game will run indefinetly. Here is an example:
```python
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
```
Call both `pygame.quit()` and `sys.exit()` to **close the pygame window and the python script respectively**.

### Event Objects
A Pygame **“Event” occurs when the user performs a specific action**, such as clicking a mouse or pressing a keyboard button. **Pygame records each and every event that occurs**. The programmer decides how the game should react to events.

`pygame.event.get()` returns a list of `pygame.event.Event` objects.

**Each event has a `type`, an attribute that tells us what kind of event has occurred**. `event.type == QUIT` from the code snippet above is an example of a `type`.

We can **create custom events** as well.\

### Creating a Display Screen
For every game, we **create a window of a fixed size** by passing a tuple containing the width and height into `display.set_mode()`.

```python
DISPLAYSURF = pygame.display.set_mode((300,300))
```

(0,0) is the top-left most corner of the window in this coordinate system. The maximum x-point and maximum y-point is the bottom-right corner (in this case (300, 300)).

### Colors
**Colors are a big part of any game development framework or engine**.

Pygame uses the RGB (Red, Green, Blue) system of colors. The values for each color range from 0 – 255, a total of 256 values.

In Pygame, we create `Color` objects by passing in a tuple containing the RGB values. For example, 
```python
color1 = pygame.Color(0, 0, 0)         # Black
color2 = pygame.Color(255, 255, 255)   # White
color3 = pygame.Color(128, 128, 128)   # Grey
color4 = pygame.Color(255, 0, 0)       # Red
```

### Frames per second
Computers can complete millions of loop cycles in under a second. This is too fast for humans. As reference, movies are run at 24 **frames per second (fps)**. Anything less than that will have an obvious stutter to it, whereas values over 100 may cause the things to move too fast for us to see.

**If we do not impose a fps limitation, the computer will execute the game loop as many times as in can** within a second. This scenario is problematic, because the frame rate will fluctuate greatly throughout the game depending on what’s currently happening (number of objects on screen, player moving or not, etc.)

To **limit fps we use the `tick(fps)` method**  where fps is an integer.

```python
FPS = pygame.time.Clock()
FPS.tick(60)
```

**Aim for fps in a range of 30 - 60.**

### Rects & Collision Detection
In every game, **each object has fixed boundaries that define the space that it currently occupies**. These fixed boundaries are essential when the **object interacts or “collides” with other objects**.

By defining such boundaries, **a game can detect when two or more boundaries overlap or touch**. This allows it to then handle the interact based on which objects are touching, such as a player picking up an item, or attacking another entity.

There are **functions to check for collisions**. For example, the code below checks for collisions between two Rects.

```python
object1 = pygame.Rect((20, 50), (50, 100))
object2 = pygame.Rect((10, 10), (100, 100))
 
print(object1.colliderect(object2))
```

This example checks for a collision between a Rect and a coordinate
```python
object1 = pygame.Rect((20, 50), (50, 100))
 
print(object1.collidepoint(50, 75))
```

We can even **create Rects based on an image's dimensions**.