# PyGame Tutorial - Event handling
source: http://pygametutorials.wikidot.com/tutorials-three

## Events
* We want the game to perform its tasks regardless of user input.
* A user can interact at any given point with the game. Examples include: displaying the main menu, painting the next frame, or computing game logic.
* PyGame will store user input in **containers called Events**. 
* **Events come in many forms**, such as a key being pressed, a mouse motion, or a mouse button being clicked.
* **Each event has a type** that stores data specific to that type of event.
* **Events are generated for each user generated input**. So pressing multiple keys will generate multiple events, as will pressing one key multiple times.