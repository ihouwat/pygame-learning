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

## Additional Reading
* [Pygame surface creation](https://coderslegacy.com/python/pygame-surface/)
