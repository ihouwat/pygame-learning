from dataclasses import dataclass

from game_objects.models.puzzle import Puzzle


@dataclass (kw_only=True)
class Level:
  """ Represents a level in the game.

  Attributes:
    puzzle (Puzzle): The puzzle to be played in the level.
    max_score (int): The maximum score that can be achieved in the level.
    level_number (int): The level number.
    score (int): The current score.
  """

  puzzle: Puzzle
  max_score: int
  level_number: int
  score: int = 0
  
  def reset_sprites(self) -> None:
    """ Generate new sprites based on puzzle."""
    return self.puzzle.generate()
    
  
  def increment_score(self, points: int) -> int:
    """ Increments the score by a given number of points."""
    self.score = self.score + points
    print(f'new score for level {self.level_number}: {self.score}')
    return self.score

  def is_completed(self) -> bool:
    """ Returns True if the level is completed, False otherwise."""
    return self.score == self.max_score
