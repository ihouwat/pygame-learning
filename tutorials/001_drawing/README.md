# PyGame Tutorial - Drawing on the screen
source: http://pygametutorials.wikidot.com/tutorials-two

## Drawing
* In PyGame, images are stored as `Surface`. A display can be treated as an ordinary image and simplifies screen management.

* PyGame coordinate system
	* Top left corner is (0,0), top right is (640, 0), bottom left is (0, 480), bottom right is (640, 480) if the window is set to (640, 480).
	* You can set a different screen size with `pygame.display.set_mode((width, height))`

* To draw something:
	1. load an image from a file
	2. blit the image on a display surface
	3. update the display.

* `Blitting`: process of drawing one image onto another. [See the docs for `pygame.Surface.blit()`](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit)

* use `convert()` when drawing `Surface` objects. When drawing surfaces to the screen, they are converted to the same pixel format as your final display. This conversion takes place every time we draw a surface, which takes time. To resolve this issue, when loading images in Pygame, we can convert them using this funcition. This removes the need to convert the image every time we draw it.

## Additional Reading
* [Pygame surface creation](https://coderslegacy.com/python/pygame-surface/)
