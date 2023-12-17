
from game_objects.models.puzzle import Puzzle
from game_objects.entities.puzzles import ColoredShapesPuzzle, ColorPuzzle, ManyItemTypesPuzzle, ShapePuzzle, SingleItemTypePuzzle, GrayscaleItemPuzzle, SpokenWordPuzzle


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

