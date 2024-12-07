from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import os
import pygame
import time
import random
import math
from copy import deepcopy
from pprint import pprint
import numpy as np
import _2048
from _2048.game import Game2048
from _2048.manager import GameManager
from AI_Minimax import maximize
from AI_MonteCarloTreeSearch import monte_carlo_tree_search
import sys

# events using pygame key
EVENTS = [
    pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}),    # UP
    pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}), # RIGHT
    pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}),  # DOWN
    pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})   # LEFT
]

CELLS = [
	[(r, c) for r in range(4) for c in range(4)], # UP: 
	[(r, c) for r in range(4) for c in range(4 - 1, -1, -1)], # RIGHT
	[(r, c) for r in range(4 - 1, -1, -1) for c in range(4)], # DOWN
	[(r, c) for r in range(4) for c in range(4)], # LEFT
]

'''
	Generator for the possible movement from the current cell
	For up/down event, will track the colum. For left/right, will track the row
	ex) if we do GET_DELTAS[0](0,0) (move up to the (0,0)), this will generate (1,0) -> (2,0) -> (3,0)
			because we would check the move/merge of the closest tile from (0,0) first.
	ex) if we do GET_DELTAS[1](1,0) (move right to (1,0)), this will generate nothing (since it's at the leftmost column)
'''  
GET_DELTAS = [
	lambda r, c: ((i, c) for i in range(r + 1, 4)), # UP
	lambda r, c: ((r, i) for i in range(c - 1, -1, -1)), # RIGHT
	lambda r, c: ((i, c) for i in range(r - 1, -1, -1)), # DOWN
	lambda r, c: ((r, i) for i in range(c + 1, 4)) # LEFT
]

import csv

def run_game(game_class=Game2048, title='2048!', data_dir='save', algorithm="minimax"):
    '''
    Runs the 2048 game for one AI player using the specified algorithm (Minimax or MCTS).
    '''
    # initialize pygame
    pygame.init()
    pygame.display.set_caption(title)
    pygame.display.set_icon(game_class.icon(32))
    clock = pygame.time.Clock()

    # directory to save game grid and max score
    os.makedirs(data_dir, exist_ok=True)

    screen = pygame.display.set_mode((game_class.WIDTH, game_class.HEIGHT))

    csv_file = os.path.join(data_dir, 'game_results.csv')
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Run", "Total Moves", "Final Score", "Highest Tile"])  # Header

    def reset_game():
        
        return GameManager(Game2048, screen,
                           os.path.join(data_dir, '2048.score'),
                           os.path.join(data_dir, '2048.%d.state'))

    manager = reset_game()

    # speed up animation
    manager.game.ANIMATION_FRAMES = 3
    manager.game.WIN_TILE = 99999

    run_count = 1
    while True:  # loop for restarting the game after it ends
        tick = 0
        total_moves = 0
        running = True

        while running:
            clock.tick(120)
            tick += 1

            if tick % 5 == 0:
                old_grid = deepcopy(manager.game.grid)

                # decide moves based on the selected algorithm
                if algorithm == "minimax":
                    best_move, _ = maximize(old_grid)
                elif algorithm == "mcts":
                    best_move, _ = monte_carlo_tree_search(old_grid)

                if best_move is None:
                    final_score = manager.game.score
                    highest_tile = np.max(manager.game.grid)

                    with open(csv_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([run_count, total_moves, final_score, highest_tile])

                    print(f"Game Over! Run: {run_count}, Total Moves: {total_moves}, Final Score: {final_score}, Highest Tile: {highest_tile}")

                    run_count += 1
                    manager = reset_game()  # reset game
                    break

                total_moves += 1
                e = EVENTS[best_move]
                manager.dispatch(e)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    total_moves = 0
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONUP:
                    manager.dispatch(event)

            manager.draw()


if __name__ == "__main__":
    try:
        gameType = sys.argv[1]
        if gameType == "-m":
            print("Run with Minimax and Alpha-Beta Pruning")
            run_game(algorithm="minimax")
        elif gameType == "-mc":
            print("Run with Monte Carlo Tree Search")
            run_game(algorithm="mcts")
    except IndexError:
        print("""Invalid option, try again with these options:
        [-m] to play with Minimax
        [-mc] to play with Monte Carlo Tree Search""")
        sys.exit(1)
