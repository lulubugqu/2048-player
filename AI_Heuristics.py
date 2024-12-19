import numpy as np, math
from copy import deepcopy

def heuristics(grid, num_empty):
    '''
    Scores the grid for Minimax.
    '''
    PATTERN_WEIGHT = 1.0
    SMOOTHNESS_WEIGHT = 0.1
    FREE_CELLS_WEIGHT = 2.7
    CORNER_WEIGHT = 2.0
    MONOTONICITY_WEIGHT = 1.0 
    
    # check grid is an array
    grid = np.array(grid)  

    pattern_score_value = PATTERN_WEIGHT * pattern_score(grid)
    smoothness_score_value = SMOOTHNESS_WEIGHT * smooth_score(grid)
    free_cells_score_value = FREE_CELLS_WEIGHT * num_empty
    corner_score_value = CORNER_WEIGHT * largest_val_in_corner(grid)
    monotonicity_score_value = MONOTONICITY_WEIGHT * monotonicity_score(grid)

    total_score = (pattern_score_value +
                   smoothness_score_value +
                   free_cells_score_value +
                   corner_score_value +
                   monotonicity_score_value)

	
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

def smooth_score(grid):
    '''
    Dock off points for grids with large differences between adjacent tiles.
    '''
    score = 0

    for col in range(4): # for all tiles
        for row in range(4):
            # if not empty tile
            if grid[col][row] != 0:  
                # log of tile value for consistent scoring
                value = np.log2(grid[col][row])  

                # check right one and down one
                for direction in [(1, 0), (0, 1)]:  # (dirCol, dirRow)
                    dirCol, dirRow = direction
                    newCol, newRow = col + dirCol, row + dirRow

                    # find next occupied tile
                    while 0 <= newCol < 4 and 0 <= newRow < 4 and grid[newCol][newRow] == 0:
                        newCol, newRow = newCol + dirCol, newRow + dirRow

                    # if target cell is valid, calc smoothness
                    if 0 <= newCol < 4 and 0 <= newRow < 4 and grid[newCol][newRow] != 0:
                        target_value = np.log2(grid[newCol][newRow])
                        # penalty for lack of smoothness
                        score -= abs(value - target_value)
    # negative score = less smooth
    return score

def largest_val_in_corner(grid):
    '''
    Bonus to grid w the largest tile is in the bottom-right corner.
    '''

    max_value = np.max(grid)
    return 1 if grid[3][3] == max_value else 0


def monotonicity_score(grid):
    '''
    Measures how monotonic the grid is. Penalize lower monotonicity.
    '''
    grid = np.array(grid)
    mono_scores = [0, 0, 0, 0]  # up, down, left, right

    # vertical mono
    for col in range(4): # for each tile
        current = 0
        next = current + 1
        while next < 4:
            # ignore empty tiles
            while next < 4 and grid[next][col] == 0:
                next += 1
            if next >= 4:
                break
            
            current_value = np.log2(grid[current][col]) if grid[current][col] != 0 else 0
            next_value = np.log2(grid[next][col]) if grid[next][col] != 0 else 0
            
            # up
            if current_value > next_value:
                mono_scores[0] += next_value - current_value
            # down
            elif next_value > current_value:
                mono_scores[1] += current_value - next_value
            
            current = next
            next += 1

    # horizontal mono
    for row in range(4):
        current = 0
        next = current + 1
        while next < 4:
            # ignore empty tiles
            while next < 4 and grid[row][next] == 0:
                next += 1
            if next >= 4:
                break
            
            current_value = np.log2(grid[row][current]) if grid[row][current] != 0 else 0
            next_value = np.log2(grid[row][next]) if grid[row][next] != 0 else 0
            
            # left
            if current_value > next_value:
                mono_scores[2] += next_value - current_value
            # right
            elif next_value > current_value:
                mono_scores[3] += current_value - next_value
            
            current = next
            next += 1

    # compile scores
    return max(mono_scores[0], mono_scores[1]) + max(mono_scores[2], mono_scores[3])
