# Pygame Arcade Launcher

A collection of classic arcade games built with Pygame, featuring a unified launcher interface.

## Games Included

- **Galactic Defenders**: Advanced space shooter with multiple enemy types and boss battles
- **Space Invaders**: Classic shoot-em-up where you defend against alien invaders
- **Tetris**: Arrange falling blocks to create complete lines
- **Car Racing**: Avoid obstacles in this top-down racing game
- **Multiplayer Snake**: Classic snake game with single and two-player modes

## Project Structure

```
pygame_arcade_launcher/
│
├── launcher.py                # Main launcher window (game selector GUI)
├── main.py                    # Entry point to run the launcher
│
├── assets/                    # Common shared assets (icons, fonts, etc.)
│   ├── images/
│   └── sounds/
│
├── core/                      # Shared logic (e.g., game manager, utils)
│   ├── game_manager.py
│   └── utils.py
│
├── games/                     # All individual games in their own folders
│   ├── space_invaders/
│   │   ├── __init__.py
│   │   ├── main.py            # Starts the Space Invaders game
│   │   └── assets/
│   │       ├── images/
│   │       └── sounds/
│   │
│   ├── tetris/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── assets/
│   │       ├── images/
│   │       └── sounds/
│   │
│   ├── car_racing/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── assets/
│   │       ├── images/
│   │       └── sounds/
│   │
│   └── multiplayer_snake/
│       ├── __init__.py
│       ├── main.py
│       └── assets/
│           ├── images/
│           └── sounds/
│
└── README.md                  # Project documentation
```

## How to Run

1. Make sure you have Python and Pygame installed:
   ```
   pip install pygame
   ```

2. Run the launcher:
   ```
   python main.py
   ```

## Controls

### Launcher
- Use mouse to select games
- ESC to quit

### Space Invaders
- LEFT/RIGHT: Move ship
- SPACE: Shoot
- ESC: Return to launcher

### Tetris
- LEFT/RIGHT: Move piece
- UP: Rotate piece
- DOWN: Soft drop
- SPACE: Hard drop
- ESC: Return to launcher

### Car Racing
- Arrow keys: Control car
- SPACE: Restart after game over
- ESC: Return to launcher

### Multiplayer Snake
- Player 1: WASD keys
- Player 2: Arrow keys
- P: Pause game
- R: Restart game
- 1: Switch to single player
- 2: Switch to two players
- ESC: Return to launcher

## Adding New Games

To add a new game:

1. Create a new folder in the `games/` directory
2. Add `__init__.py` and `main.py` files
3. Implement a `main()` function that returns the score
4. Add game assets in an `assets/` subfolder

The game will automatically appear in the launcher.

## Future Improvements

- High score tracking
- Game settings and configuration
- Sound effects and music
- More games!

## License

This project is open source and available under the MIT License.
