import numpy as np, math
from copy import deepcopy

COUNT_X = 4
COUNT_Y = 4

pattern = [[0, 0, 1, 3],
            [0, 1, 3, 5],
            [1, 3, 5, 15],
            [3, 5, 15, 30]]

corner = [[0.0, 0.0, 0.1, 0.1],
          [0.0, 0.1, 0.1, 0.3],
          [0.1, 0.1, 0.3, 0.5],
          [0.1, 0.3, 0.5, 1]]

def heuristics(grid, num_empty):
  '''
  This function scores the grid based on the algorithm implemented
  so that the maximize function of AI_Minimax can decide which branch
  to follow.
  '''
  grid = np.array(grid)
  score = 0

  # TODO: Implement heuristics here.  
  
  p_score = pattern_score(grid)
  s_score = smooth_score(grid)
  corner = largest_value_in_corner(grid)
  
  # Weight for each score

  score += p_score
  score += s_score  

  return score


def pattern_score(grid):
  score = 0
  for x in range(4):
    for y in range(4):
      score += grid[x][y] * pattern[x][y]

  return score

def smooth_score(grid):
  score = 0

  score -= np.sum(abs(grid[:, 0] - grid[:, 1]))
  score -= np.sum(abs(grid[:, 1] - grid[:, 2]))
  score -= np.sum(abs(grid[:, 2] - grid[:, 3]))

  score -= np.sum(abs(grid[0, :] - grid[1, :]))
  score -= np.sum(abs(grid[1, :] - grid[2, :]))
  score -= np.sum(abs(grid[2, :] - grid[3, :]))

  return score 

def largest_value_in_corner(grid):
  max_value = 0
  for x in range(4):
    for y in range(4):
      if max_value < grid[y][x]:
        max_value = grid[y][x]
  
  if grid[3][3] == max_value:
    return True
  return False