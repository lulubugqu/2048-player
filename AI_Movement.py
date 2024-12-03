def free_cells(grid):
    '''
    Returns the list of coordinates of empty cells
    '''
    return [(x, y) for x in range(4) for y in range(4) if not grid[y][x]]

def move(grid, action):
    '''
    Makes the action based on the action. A tile would keep moving
    till it get merged (if both tiles have the same value), reached to
    the edge of the grid, or got stopped by some other tile (with different value).
    '''
    # imported required functions here to avoid circular import error
    from AI_game import CELLS, GET_DELTAS

    actiond, sum = 0, 0

    # For the [upper/bottom/left/right]most tile for each row/column
    for row, column in CELLS[action]:
        # for each movement from the cell on [below/above/right/left]
        for dr, dc in GET_DELTAS[action](row, column):
            # If the current tile is blank:
            if not grid[row][column] and grid[dr][dc]:
                # move the tile to the new position.
                grid[row][column], grid[dr][dc] = grid[dr][dc], 0
                actiond += 1

            # If there exists a tile:    
            if grid[dr][dc]:
                # If the tile can merge with the current tile:
                if grid[row][column] == grid[dr][dc]:
                    grid[row][column] *= 2
                    grid[dr][dc] = 0
                    sum += grid[row][column]
                    actiond += 1
                # When hitting a tile we stop trying.
                break
    return grid, actiond, sum