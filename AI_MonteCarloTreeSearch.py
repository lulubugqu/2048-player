import random
from copy import deepcopy
import numpy as np
from AI_Movement import move, free_cells

SIMULATIONS = 50  # reduced number of simulations per move
DEPTH = 2  # reduced simulation depth

def simulate(grid):
    '''
    Simulates a random game from the current grid and returns the final score.
    '''
    grid = deepcopy(grid)
    for _ in range(DEPTH):
        valid_moves = []
        for i in range(4):  # iterate over possible moves (0: UP, 1: RIGHT, 2: DOWN, 3: LEFT)
            new_grid = deepcopy(grid)
            if move(new_grid, i):
                valid_moves.append((i, new_grid))
        if not valid_moves:  # end simulation if no more valid moves
            break
        _, grid = random.choice(valid_moves)
        if np.max(grid) >= 2048:  # stop simulation early if the 2048 tile is achieved
            break
    return np.max(grid) + len(free_cells(grid))  # reward more empty cells


def check_same(old_grid, new_grid):
    for i in range(len(old_grid)):
        for j in range(len(old_grid[i])):
            if old_grid[i][j] != new_grid[i][j]:
                return False
    return True


def monte_carlo_tree_search(grid):
    '''
    Performs MCTS to find the best move for the current grid.
    '''
    scores = [0] * 4  # scores for UP, RIGHT, DOWN, LEFT
    moves_made = [False] * 4  # track if moves result in a change

    for move_index in range(4):
        for _ in range(SIMULATIONS):
            new_grid = deepcopy(grid)
            if move(new_grid, move_index) and not check_same(grid, new_grid):
                moves_made[move_index] = True
                scores[move_index] += simulate(new_grid)

    # find move with the highest average score among valid moves
    valid_moves = [i for i in range(4) if moves_made[i]]
    if not valid_moves:
        return None, 0  # game over if no valid moves

    best_move = max(valid_moves, key=lambda i: scores[i])
    return best_move, scores[best_move]
