import numpy as np, math
from copy import deepcopy

def heuristics_ab(grid, num_empty):
    """
    Scores the grid for Minimax.
    """
    PATTERN_WEIGHT = 0.3 
    MONOTONICITY_WEIGHT = 2.7
    SMOOTHNESS_WEIGHT = 0.7
    FREE_TILES_WEIGHT = 2.1
    CORNER_WEIGHT = 2.2
    MONOTONICITY_BONUS_WEIGHT = 0.5


    grid = np.array(grid)
    pattern_score_value = PATTERN_WEIGHT * pattern_score(grid)
    monotonicity_score = MONOTONICITY_WEIGHT * monotonicity_ab(grid)
    smoothness_score = SMOOTHNESS_WEIGHT * smoothness_ab(grid)
    corner_score_value = CORNER_WEIGHT * largest_val_in_corner(grid)
    free_tiles_score = FREE_TILES_WEIGHT * num_empty
    # monotonicity_bonus_value = MONOTONICITY_BONUS_WEIGHT * monotonicity_bonus(grid)

    total_score = corner_score_value + monotonicity_score + smoothness_score + free_tiles_score
    return total_score

def pattern_score(grid):
    '''
    Calc weighted pattern score based on predefined weights.
    '''
    pattern = [[0, 0, 1, 3],
               [0, 1, 3, 5],
               [1, 3, 5, 15],
               [3, 5, 15, 30]]
    score = 0
    for col in range(4):
        for row in range(4):
            score += grid[col][row] * pattern[col][row]
    return score


def largest_val_in_corner(grid):
    '''
    Bonus to grid w the largest tile is in the bottom-right corner.
    '''
    
    max_value = np.max(grid)
    return 1 if grid[3][3] == max_value else 0

def monotonicity_ab(grid):
    """
    measure of how monotonic the grid is.
    """
    score = 0
    # penalty breaking mono in columns
    for col in grid.T:
        for i in range(len(col) - 1):
            if col[i] > col[i + 1]:
                score -= abs(col[i] - col[i + 1])

    # penalty for breaking mono in rows
    for row in grid:
        for i in range(len(row) - 1):
            if row[i] > row[i + 1]:
                score -= abs(row[i] - row[i + 1])
    return score

def smoothness_ab(grid):
    """
    Measures how smooth the grid is. Penalty to large differences between adjacent tiles.
    """
    score = 0
    
    # penalty for large differences vert
    for col in grid.T:
        for i in range(len(col) - 1):
            score -= abs(col[i] - col[i + 1])

    # penalty for  differences horizontally
    for row in grid:
        for i in range(len(row) - 1):
            score -= abs(row[i] - row[i + 1])

    return score
