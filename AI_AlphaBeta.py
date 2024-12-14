from copy import deepcopy
import numpy as np, math
from AI_Movement import free_cells, move
# from AI_Heuristics import heuristics_ab
from AI_Heuristics import heuristics
    # # Important H
    # Tile monotonicity (higher tiles near the edges or corners)
    # Smoothness (adjacent tiles with small differences)
    # Free cells count (to prioritize grids with more moves)
    # Max tile placement (to avoid blocking higher values)

# DEPTH = 6

def adaptive_depth(num_empty):
    if num_empty >= 8:
        return 5
    elif num_empty >= 4:
        return 4
    else:
        return 3

def check_same(old_grid, new_grid):
    if np.array_equal(old_grid, new_grid):
         return True
    return False
    # for i in range(len(old_grid)):
    #     for j in range(len(old_grid[i])):
    #         if old_grid[i][j] != new_grid[i][j]:
    #             return False
    # return True

def maximize_ab(grid, depth=0, alpha=float('-inf'), beta=float('inf')):
    empty_cells = free_cells(grid)
    num_empty = len(empty_cells)

    max_depth = adaptive_depth(num_empty) # calc depth depending on num_empty

    if depth >= max_depth or num_empty == 0:
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
    max_depth = adaptive_depth(num_empty) # calc depth depending on num_empty

    if depth >= max_depth or num_empty == 0:
        return None, heuristics_ab(grid, num_empty)
    
    # unneccesary because of ab prunign
    # if num_empty >= 6 and depth >= 3: 
    #     return None, heuristics_ab(grid, num_empty)

    best_score = float('inf')

    for c, r in empty_cells:
        child_scores = []
        for v in [2, 4]:
            original_value = grid[c][r]
            grid[c][r] = v
            _, child_score = maximize_ab(grid, depth + 1, alpha, beta)
            grid[c][r] = original_value 
            
            weight = (0.9 / num_empty) if v == 2 else (0.1 / num_empty)
            child_scores.append(child_score * weight)

        best_score = min(best_score, sum(child_scores))
        beta = min(beta, best_score)
        if beta <= alpha:
            # print(f"PRUNING in MIN at depth {depth}: best_score={best_score}, alpha={alpha}, beta={beta}")
            break

    return None, best_score