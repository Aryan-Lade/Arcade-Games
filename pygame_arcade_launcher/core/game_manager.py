#!/usr/bin/env python3
"""
Game Manager for the Pygame Arcade Launcher.
Handles loading, managing, and launching games.
"""
import os
import importlib
import pygame

class GameManager:
    """Manages the collection of available games."""
    
    def __init__(self):
        """Initialize the game manager and discover available games."""
        self.games_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'games')
        self.games = []
        self.discover_games()
    
    def discover_games(self):
        """Scan the games directory and identify available games."""
        if not os.path.exists(self.games_dir):
            print(f"Games directory not found: {self.games_dir}")
            return
        
        # Look for game directories
        for game_dir in os.listdir(self.games_dir):
            game_path = os.path.join(self.games_dir, game_dir)
            
            # Check if it's a directory and has a main.py file
            if os.path.isdir(game_path) and os.path.exists(os.path.join(game_path, 'main.py')):
                # Format the game name for display (replace underscores with spaces, capitalize)
                display_name = ' '.join(word.capitalize() for word in game_dir.split('_'))
                
                # Get thumbnail path if it exists
                thumbnail_path = os.path.join(game_path, 'assets', 'images', 'thumbnail.png')
                thumbnail = thumbnail_path if os.path.exists(thumbnail_path) else None
                
                # Add game to the list
                self.games.append({
                    'id': game_dir,
                    'name': display_name,
                    'path': game_path,
                    'module': f"games.{game_dir}.main",
                    'thumbnail': thumbnail
                })
    
    def get_available_games(self):
        """Return the list of available games."""
        return self.games
    
    def load_game(self, game_id):
        """
        Load a game module by its ID.
        
        Args:
            game_id (str): The ID of the game to load
            
        Returns:
            module: The loaded game module, or None if not found
        """
        for game in self.games:
            if game['id'] == game_id:
                try:
                    return importlib.import_module(game['module'])
                except ImportError as e:
                    print(f"Error importing game {game_id}: {e}")
                    return None
        
        print(f"Game not found: {game_id}")
        return None
