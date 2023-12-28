import pygame
from audio.audio_player import AudioPlayer
from engine.animation_engine import AnimationEngine
from engine.event_listener import EventListener
from engine.renderer import Renderer
from game import Game
from game_objects.level import Level
from game_objects.puzzles import (
    ColoredShapesPuzzle,
    ColorPuzzle,
    GrayscaleItemPuzzle,
    ManyItemTypesPuzzle,
    Puzzle,
    ShapePuzzle,
    SingleItemTypePuzzle,
    SpokenWordPuzzle,
)
from models.game_types import Language
from ui.game_menu import GameMenu
from ui.status_bar import StatusBar
from ui.ui_display import UIDisplay

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

# initialize levels, game, clock
frames_per_sec = pygame.time.Clock()
levels: list[Level] = [ Level(puzzle=puzzle, level_number=i+1, max_score=2) for i, puzzle in enumerate(puzzles) ]
game = Game(
    renderer=Renderer(),
    ui_display=UIDisplay(),
    animation_engine=AnimationEngine(),
    audio_player=AudioPlayer(),
    event_listener=EventListener(),
    status_bar=StatusBar(x_coordinate=10, y_coordinate=10),
    game_menu=GameMenu(),
    levels=levels,
    language=Language.ENGLISH,
    )