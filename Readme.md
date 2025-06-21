# Arcade Games

A collection of classic arcade games built with Pygame, featuring a unified launcher interface.

## Project Overview

This repository contains a modular arcade game launcher with multiple classic games implemented in Python using Pygame. Each game is self-contained within its own directory, making it easy to add new games or modify existing ones.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Pygame 2.1.0 or higher

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Arcade-Games.git
   cd Arcade-Games
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the launcher:
   ```
   python pygame_arcade_launcher/main.py
   ```

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

## Adding New Games

To add a new game:

1. Create a new folder in the `games/` directory
2. Add `__init__.py` and `main.py` files
3. Implement a `main()` function that returns the score
4. Add game assets in an `assets/` subfolder

The game will automatically appear in the launcher.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Pygame community for the excellent game development library
- Classic arcade game designers for the inspiration
