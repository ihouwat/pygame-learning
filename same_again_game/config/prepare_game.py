import pygame
from audio.audio_player import AudioPlayer
from engine.animation_engine import AnimationEngine
from engine.animator import Animator
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
)
from models.game_types import Language, Soundtrack, SoundType
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
]

soundtrack: Soundtrack = {
	SoundType.INTRO: ["alexander-nakarada-silly-intro(chosic.com).mp3"],
	SoundType.GAME_MUSIC: [
		"Monkeys-Spinning-Monkeys(chosic.com).mp3",
		"Run-Amok(chosic.com).mp3",
		"Silly-Fun(chosic.com).mp3",
		"Pixelland(chosic.com).mp3"
	],
	SoundType.EFFECTS: [
		"644953__craigscottuk__quiz-gameshow-correct-ring-01.mp3",
		"178610__petillo__short-audience-applause.mp3",
		"131657__bertrof__game-sound-wrong.wav"
	],
	SoundType.VICTORY: ["Fluffing-a-Duck(chosic.com).mp3"],
}

# initialize levels, game, clock
frames_per_sec = pygame.time.Clock()
levels: list[Level] = [ Level(puzzle=puzzle, level_number=i+1, max_score=5) for i, puzzle in enumerate(puzzles) ]
game = Game(
	renderer=Renderer(),
	ui_display=UIDisplay(),
	animator=Animator(animation_engine=AnimationEngine()),
	audio_player=AudioPlayer(),
	event_listener=EventListener(),
	status_bar=StatusBar(x_coordinate=10, y_coordinate=10),
	game_menu=GameMenu(),
	levels=levels,
	language=Language.ENGLISH,
	soundtrack=soundtrack
)