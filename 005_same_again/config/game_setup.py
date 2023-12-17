
from game_objects.entities.puzzles import (
    ColoredShapesPuzzle,
    ColorPuzzle,
    GrayscaleItemPuzzle,
    ManyItemTypesPuzzle,
    ShapePuzzle,
    SingleItemTypePuzzle,
    SpokenWordPuzzle,
)
from game_objects.models.puzzle import Puzzle

# MOVE TO SOME SETUP FUNCTION
puzzles: list[Puzzle] = [
	ColorPuzzle(), 
	ShapePuzzle(),
	ColoredShapesPuzzle(),
	SingleItemTypePuzzle(),
	ManyItemTypesPuzzle(),
	GrayscaleItemPuzzle(),
	SpokenWordPuzzle(),
]

