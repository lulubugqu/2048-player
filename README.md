# 2048 AutoPlayer

Automated player for the 2048 game using Selenium in Python.

## Description

This repository contains a Python script that automates gameplay for the popular 2048 game available at [2048game.com](https://2048game.com/). The script uses the Selenium WebDriver to interact with the game elements and simulate key presses to play the game.

## Features

- Automated gameplay: The script automatically plays the 2048 game by sending key presses (up, down, left, right) to combine tiles and achieve the highest possible score.
- Game over detection: It detects when the game is over and automatically restarts the game by clicking the "Play Again" button.
- Game won detection: It also detects when the game is won and stops gameplay, waiting on the game over screen.

## Requirements

- Python 3.x
- Selenium WebDriver
- Firefox web browser (can also use Chrome; change line 70)
- WebDriver executable (geckodriver for Firefox, chromedriver for Chrome)

## Usage

1. Install Python 3.x.

2. Install Selenium WebDriver using pip:
   `pip install selenium`

4. Download the WebDriver executable for your preferred browser:
- [geckodriver (Firefox)](https://github.com/mozilla/geckodriver/releases)
- [chromedriver (Chrome)](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  
4. Clone this repository:
  `git clone https://github.com/hasibshaif/2048_automator.git`

5. Navigate to the repository directory:
   `cd 2048-AutoPlayer`

6. Run the script:
 `python automate_2048.py`







