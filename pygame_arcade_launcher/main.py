#!/usr/bin/env python3
"""
Main entry point for the Pygame Arcade Launcher.
This script initializes the application and starts the launcher GUI.
"""
import pygame
import sys
from launcher import ArcadeLauncher

def main():
    """Initialize pygame and start the arcade launcher."""
    pygame.init()
    
    # You could add splash screen, logging setup, etc. here
    
    # Start the launcher
    launcher = ArcadeLauncher()
    launcher.run()
    
    # Clean up when done
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
