# 2048 AutoPlayer
Automated player for the 2048 game using Python and Pygames.

## Description

Used base code from https://github.com/Maanuj-Vora/2048-AI-Minimax. Modified to test different heuristics, add functionality for measuring evaluation metrics, implemented alpha-beta pruning monte carlo tree search algorithms.

## How to run
### Dependencies
1. Python
2. Pip
3. This is built based on the 2048 pypi package made by user 'quantum'. If you don't have this package on your laptop, run this command in terminal for necessary dependencies.
```
pip install 2048
```
### Play
Then, in the directory, run either command see the game in action with different algrithms, use 
  -m for MiniMax
  -ab for MiniMax with Alpha-Beta Pruning
  -mc for Monte Carlo Tree Search
```
python AI_game.py -m
python AI_game.py -ab 
python AI_game.py -mc 
```
With this the GUI will pop up, and AI will start playing the game. It will restart when it loses and continue playing nonstop until it wins the game. 

To explore different depth levels for MiniMax, that value can be modified from AI_Minimax and AI_AlphaBeta files.


## Code Base Description
| File | Description |
| --- | --- |
| User_game | The traditional one-human-player 2048 game, takes in keyboard input. |
| AI_game | Run one-AI-player 2048 game. |
| AI_Move | Basic tile move/merge logic based on 2048 rules. |
| AI_Minimax | Minimax algorithm for 2048 tree. Max is the AI playing the game, and Min is the computer which generates new 2 or 4 tile randomly. |
| AI_Heuristics | Heuristics function to rank/compare possible branch grids. This will be used to collect the best possible move in AI_Minimax. |
| AI_AlphaBeta | Minimax with Alpha Beta pruning. |
| AI_MonteCarloTreeSearch | MCTS algorithm for 2048 tree. |


