import pygame
from engine.event_handler import EventListener
from engine.renderer import Renderer
from game import Game
from game_objects.entities.level import Level
from game_objects.entities.puzzles import (
    ColoredShapesPuzzle,
    ColorPuzzle,
    GrayscaleItemPuzzle,
    ManyItemTypesPuzzle,
    Puzzle,
    ShapePuzzle,
    SingleItemTypePuzzle,
    SpokenWordPuzzle,
)
from game_objects.entities.status_bar import StatusBar

# initialize game
pygame.init()

# list of puzzles to construct levels with
puzzles: list[Puzzle] = [
	ColorPuzzle(), 
	ShapePuzzle(),
	ColoredShapesPuzzle(),
	SingleItemTypePuzzle(),
	ManyItemTypesPuzzle(),
	GrayscaleItemPuzzle(),
	SpokenWordPuzzle(),
]

# initialize levels, game, and, clock
frames_per_sec = pygame.time.Clock()
levels = [ Level(puzzle=puzzle, level_number=i+1, max_score=4) for i, puzzle in enumerate(puzzles) ]
game = Game(
    renderer=Renderer(),
    event_listener=EventListener(),
    status_bar=StatusBar(rect=pygame.Rect(0, 0, 800, 50)),
    levels=levels,
    )