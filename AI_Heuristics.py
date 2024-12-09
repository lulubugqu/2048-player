import numpy as np, math
from copy import deepcopy

# COUNT_X = 4
# COUNT_Y = 4

PATTERN_WEIGHT = 1.0
SMOOTHNESS_WEIGHT = -0.1
FREE_CELLS_WEIGHT = 2.7
CORNER_WEIGHT = 5.0
MONOTONICITY_WEIGHT = 1.5 

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
    Scores the grid for Minimax.
    '''
    grid = np.array(grid)  # Ensure grid is an array
    score = 0

    # Weighted metrics
    score += PATTERN_WEIGHT * pattern_score(grid)
    score += SMOOTHNESS_WEIGHT * smooth_score(grid)
    score += FREE_CELLS_WEIGHT * num_empty
    score += CORNER_WEIGHT * largest_value_in_corner(grid)
    score += MONOTONICITY_WEIGHT * monotonicity_score(grid)

    return score

def pattern_score(grid):
    '''
    Calculates weighted pattern score based on predefined weights.
    '''
    score = 0
    for x in range(4):
        for y in range(4):
            score += grid[x][y] * pattern[x][y]
    return score

def smooth_score(grid):
    '''
    Penalizes grids with large differences between adjacent tiles.
    '''
    score = 0

    # Horizontal smoothness
    score -= np.sum(abs(grid[:, :-1] - grid[:, 1:]))

    # Vertical smoothness
    score -= np.sum(abs(grid[:-1, :] - grid[1:, :]))

    return score

def largest_value_in_corner(grid):
    '''
    Rewards grids where the largest tile is in the bottom-right corner.
    '''
    max_value = np.max(grid)
    return 1 if grid[3][3] == max_value else 0


def monotonicity_score(grid):
    '''
    Rewards grids that have increasing or decreasing values row-wise and column-wise.
    This ensures tiles are aligned for easier merges.
    '''
    score = 0

    # Row monotonicity
    for row in grid:
        for i in range(len(row) - 1):
            if row[i] > row[i + 1]:  # Penalize descending order in rows
                score -= abs(row[i] - row[i + 1])

    # Column monotonicity
    for col in grid.T:
        for i in range(len(col) - 1):
            if col[i] > col[i + 1]:  # Penalize descending order in columns
                score -= abs(col[i] - col[i + 1])

    return score