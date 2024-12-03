from copy import deepcopy
import numpy as np, math
from AI_Movement import free_cells, move
from AI_Heuristics import heuristics

DEPTH = 4

def check_same(old_grid, new_grid):
    for i in range(len(old_grid)):
        for j in range(len(old_grid[i])):
            if old_grid[i][j] != new_grid[i][j]:
                return False
    return True

def maximize(grid, depth=0):
    '''
    Maximize function for the max (AI) of the MiniMax Algorithm
    If you want to change the depth of the search tree, try to 
    implement some conditions for the "early stopping" at minimize
    or set up your own limit constant.
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
            pass
        else:
            sum_score = minimize(new_grid, depth+1)
            if sum_score > best_score:
                best_score = sum_score
                best_move = i
    
    return best_move, best_score

def minimize(grid, depth=0):
    '''
    Minimize function for the min (Computer) of the Minimax Algorithm
    Computer put new 2 tile (with 90% probability) or 
    4 tile (with 10% probability) at one of empty spaces
    '''
    empty_cells = free_cells(grid)
    num_empty = len(empty_cells)

    if depth > DEPTH:
        return heuristics(grid, num_empty)

    if num_empty == 0:
        _, new_score = maximize(grid, depth+1)
        return new_score

    if num_empty >= 6 and depth >= 3:
        return heuristics(grid, num_empty)

    sum_score = 0

    for c, r in empty_cells:
        for v in [2, 4]:
            new_grid = deepcopy(grid)
            new_grid[c][r] = v

            _, new_score = maximize(new_grid, depth+1)

            if v == 2:
                new_score *= (0.9 / num_empty)
            else:
                new_score *= (0.1 / num_empty)

            sum_score += new_score

    return sum_score