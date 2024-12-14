from copy import deepcopy
import numpy as np, math
from AI_Movement import free_cells, move
from AI_Heuristics import heuristics
# Important H

    # Smoothness (adjacent tiles should have similar values)
    # Monotonicity (values should increase/decrease in rows or columns)
    # Maximizing high-value tiles in corners
    # Minimizing empty spaces
DEPTH = 4

def check_same(old_grid, new_grid):
    return np.array_equal(old_grid, new_grid)

def maximize(grid, depth=0):
    '''
    Maximize function for the max (AI) of the MiniMax Algorithm
    '''

    empty_cells = free_cells(grid)
    num_empty = len(empty_cells)

    if depth > DEPTH:
        return None, heuristics(grid, num_empty)

    best_score = float('-inf')
    best_move = None

    for i in range(4):
        new_grid = deepcopy(grid)
        move(new_grid, i)
        if check_same(grid, new_grid):
            continue
        else:
            sum_score = minimize(new_grid, depth+1)
            if sum_score > best_score:
                best_score = sum_score
                best_move = i
    
    return best_move, best_score

def minimize(grid, depth=0):
    '''
    Minimize function for the min (Computer) of the Minimax Algorithm
    '''
    # Computer will places a new 2 tile (with 90% probability) or 
    # 4 tile (with 10% probability) at one of empty spaces
    empty_cells = free_cells(grid)
    num_empty = len(empty_cells)

    if depth > DEPTH:
        return heuristics(grid, num_empty)

    if num_empty == 0:
        _, new_score = maximize(grid, depth+1)
        return new_score

    # pruning condiiton
    if num_empty >= 6 and depth >= 3:
        return heuristics(grid, num_empty)

    sum_score = 0

    for c, r in empty_cells: # for each empty cell
        for v in [2, 4]:  # for each possible value 
            new_grid = deepcopy(grid) 
            new_grid[c][r] = v
            
            # eval outcome of the placement with maximize()
            _, new_score = maximize(new_grid, depth+1)

            if v == 2:
                new_score *= (0.9 / num_empty)
            else:
                new_score *= (0.1 / num_empty)

            sum_score += new_score

    return sum_score