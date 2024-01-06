# Minesweeper

## Overview
This program implements a classic Minesweeper game with an added AI assistant. The game includes various difficulty levels and offers a graphical interface using Pygame. The AI player can make moves based on the knowledge it accumulates during the game.

## Features
- **Graphical Interface**: Utilizes Pygame for a user-friendly gaming experience.
- **Multiple Difficulty Levels**: Options for 'easy', 'medium', and 'hard' to cater to different skill levels.
- **AI Player**: An AI component that can autonomously make safe or random moves based on its knowledge.
- **Customizable Game Settings**: Adjust the number of mines, and the height and width of the game board.

## Requirements
- Python 3.x
- Pygame Library

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install Pygame: `pip install pygame`

## Usage
- Run the `runner.py` script to start the game.
- Left-click on a cell to reveal it.
- Right-click on a cell to mark or unmark it as a mine.
- Use the AI Move button to have the AI make a move.
- Select different difficulty levels to change the game's complexity.
- Reset or go back to the main menu at any point during the game.

## Game Structure
- `Minesweeper`: Defines the game logic and maintains the game state.
- `MinesweeperAI`: Represents the AI player, capable of making moves based on logical deductions.
- `runner.py`: Contains the Pygame implementation for the user interface and game interaction.

## Files
- `minesweeper.py`: Contains the `Minesweeper` and `MinesweeperAI` classes.
- `runner.py`: Implements the Pygame interface and game loop.
- `assets/`: Directory containing fonts and images used in the game.