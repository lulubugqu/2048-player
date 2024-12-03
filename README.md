# 2048 AutoPlayer

Automated player for the 2048 game using Python and Pygames.

## Description

Used base code from https://github.com/Maanuj-Vora/2048-AI-Minimax. Modified to add functionality for evaluation and monte carlo tree search

## Code Base Description
1. User_game: The traditional one-human-player 2048 game
2. AI_game: Run one-AI-player 2048 game
3. AI_Move: the basic tile move/merge logic based on 2048 rules
4. AI_Minimax: Minimax algorithm for 2048 tree. Max is the AI playing the game, and Min is the computer which generates new 2 or 4 tile randomly
5. AI_Heuristics: The heuristics function to rank/compare possible branch grids. This will be used to collect the best possible move in AI_Minimax

## How to run/test your AI

This AI is built based on the 2048 pypi package made by user 'quantum'. If you don't have this package on your laptop, run this command in terminal for necessary dependencies.
```
pip install 2048
```

Then, in the directory, run to see AI in action.
```
python AI_game.py
```
The GUI will pop up, and AI will start playing the game.
