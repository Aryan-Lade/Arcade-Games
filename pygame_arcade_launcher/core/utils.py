#!/usr/bin/env python3
"""
Utility functions for the Pygame Arcade Launcher.
Contains helper functions used across the application.
"""
import os
import pygame

def load_image(path, scale=None, convert_alpha=True):
    """
    Load an image from the specified path.
    
    Args:
        path (str): Path to the image file
        scale (tuple, optional): Width and height to scale the image to
        convert_alpha (bool): Whether to convert the image for alpha transparency
        
    Returns:
        pygame.Surface: The loaded image
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")
            
        image = pygame.image.load(path)
        
        if convert_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
            
        if scale:
            image = pygame.transform.scale(image, scale)
            
        return image
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        # Return a placeholder surface
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf

def load_sound(path):
    """
    Load a sound effect from the specified path.
    
    Args:
        path (str): Path to the sound file
        
    Returns:
        pygame.mixer.Sound: The loaded sound, or None if loading fails
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sound not found: {path}")
            
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"Error loading sound {path}: {e}")
        return None

def draw_text(surface, text, size, color, x, y, font_name=None, align="center"):
    """
    Draw text on a surface.
    
    Args:
        surface (pygame.Surface): Surface to draw on
        text (str): Text to draw
        size (int): Font size
        color (tuple): RGB color tuple
        x (int): X position
        y (int): Y position
        font_name (str, optional): Font name or path
        align (str): Text alignment ("left", "center", or "right")
    """
    if font_name:
        try:
            font = pygame.font.Font(font_name, size)
        except:
            font = pygame.font.SysFont(None, size)
    else:
        font = pygame.font.SysFont(None, size)
        
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "center":
        text_rect.center = (x, y)
    elif align == "right":
        text_rect.right = x
        text_rect.centery = y
    else:  # left
        text_rect.left = x
        text_rect.centery = y
        
    surface.blit(text_surface, text_rect)
