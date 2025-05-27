"""
Configuration settings for the Pygame Arcade Launcher.
Centralized settings for screen dimensions, FPS, etc.
"""

# Display settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
FULLSCREEN = False

# Launcher settings
LAUNCHER_TITLE = "Pygame Arcade Launcher"
LAUNCHER_BACKGROUND_COLOR = (0, 0, 0)  # Black
LAUNCHER_TEXT_COLOR = (255, 255, 255)  # White
LAUNCHER_HIGHLIGHT_COLOR = (100, 100, 255)  # Light blue

# Game settings
DEFAULT_GAME_FPS = 60

# Audio settings
MUSIC_VOLUME = 0.5  # 50%
SOUND_VOLUME = 0.7  # 70%

# File paths
import os

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Asset directories
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

# Games directory
GAMES_DIR = os.path.join(BASE_DIR, 'games')

# Data directory (for high scores, etc.)
DATA_DIR = os.path.join(BASE_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# High score file
HIGH_SCORES_FILE = os.path.join(DATA_DIR, 'high_scores.json')
