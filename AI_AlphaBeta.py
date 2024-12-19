from copy import deepcopy
import numpy as np, math
from AI_Movement import free_cells, move
from AI_Heuristics_AlphaBeta import heuristics_ab
    # # Important H
    # Monotonicity (higher tiles near the edges or corners)
    # Smoothness (adjacent tiles have small differences)
    # Maximizing high-value tiles in corners
    # Maximize empty spaces

DEPTH = 4


def check_same(old_grid, new_grid):
    return np.array_equal(old_grid, new_grid)

def maximize_ab(grid, depth=0, alpha=float('-inf'), beta=float('inf')):
    empty_cells = free_cells(grid)
    num_empty = len(empty_cells)

    if depth >= DEPTH or num_empty == 0:
        return None, heuristics_ab(grid, num_empty)

    best_score = float('-inf')
    best_move = None

    for i in range(4):
        new_grid = deepcopy(grid)
        move(new_grid, i)
        
        if check_same(grid, new_grid):
            continue

        _, child_score = minimize_ab(new_grid, depth + 1, alpha, beta)
        if child_score > best_score:
            best_score = child_score
            best_move = i
        
        alpha = max(alpha, best_score)
        if beta <= alpha:
            # print(f"PRUNING in MAX at depth {depth}: best_score={best_score}, alpha={alpha}, beta={beta}")
            break


    return best_move, best_score

def minimize_ab(grid, depth=0, alpha=float('-inf'), beta=float('inf')):
    empty_cells = free_cells(grid)
    num_empty = len(empty_cells)

    if depth >= DEPTH or num_empty == 0:
        return None, heuristics_ab(grid, num_empty)
    
    # unneccesary because of ab prunign
    # if num_empty >= 6 and depth >= 3: 
    #     return None, heuristics_ab(grid, num_empty)

    best_score = float('inf')

    for c, r in empty_cells:
        child_scores = []
        for v in [2, 4]:
            original_value = grid[c][r]
            new_grid = deepcopy(grid) 
            new_grid[c][r] = v
            _, child_score = maximize_ab(new_grid, depth + 1, alpha, beta)
            new_grid[c][r] = original_value 
            
            weight = (0.9 / num_empty) if v == 2 else (0.1 / num_empty)
            child_scores.append(child_score * weight)

        best_score = min(best_score, sum(child_scores))
        beta = min(beta, best_score)
        if beta <= alpha:
            # print(f"PRUNING in MIN at depth {depth}: best_score={best_score}, alpha={alpha}, beta={beta}")
            break

    return None, best_score

# # test grid
# def initialize_test_grid():
#     return np.array([
#         [4, 16, 64, 4],
#         [16, 8, 512, 8],
#         [16, 8, 512, 8],
#         [2, 64, 2, 1024]
#     ])
# def initialize_test_grid2():
#     return np.array([
#         [0, 0, 0, 8],
#         [0, 0, 4, 16],
#         [4, 4, 16, 64],
#         [4, 16, 64, 128]
#  ])

# 
# def run_tests():
#     test_grid = initialize_test_grid2()
#     ab_score = heuristics_ab(test_grid, 0)
#     print(f"ab_score: {ab_score}")
#     score = heuristics(test_grid, 0)
#     print(f"score: {score}")

# # run tests when function
# run_tests()