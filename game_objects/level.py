from dataclasses import dataclass

from config.logger import logger
from models.puzzle import Puzzle


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
  
  def increment_score(self, points: int) -> int:
    """ Increments the score by a given number of points.
    
    Args:
      points (int): The number of points to increment the score by.
    """
    self.score = self.score + points
    logger.info(f'new score for level {self.level_number}: {self.score}')
    return self.score

  def is_completed(self) -> bool:
    """ Checks if the level has been completed."""
    return self.score == self.max_score
  
  def reset(self) -> None:
    """ Resets the level."""
    self.score = 0