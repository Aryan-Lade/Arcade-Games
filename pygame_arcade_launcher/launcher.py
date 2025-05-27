#!/usr/bin/env python3
"""
Main launcher window for the Pygame Arcade.
Displays a GUI with buttons/thumbnails for each available game.
"""
import pygame
import sys
import os
from core.game_manager import GameManager
from core.utils import load_image, draw_text
import importlib

class ArcadeLauncher:
    """Main launcher class for the arcade game collection."""
    
    def __init__(self):
        """Initialize the launcher window and load game data."""
        # Import config settings
        from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN, LAUNCHER_TITLE
        
        # Initialize display
        self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        
        # Set up display mode (fullscreen or windowed)
        if FULLSCREEN:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            self.is_fullscreen = True
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.is_fullscreen = False
            
        pygame.display.set_caption(LAUNCHER_TITLE)
        
        # Set up colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.HIGHLIGHT = (100, 150, 255)
        self.BUTTON_COLOR = (50, 50, 80)
        self.HOVER_COLOR = (70, 70, 120)
        self.RECORD_RED = (255, 50, 50)
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Load game manager
        self.game_manager = GameManager()
        self.games = self.game_manager.get_available_games()
        
        # Initialize recorder
        from core.recorder import GameRecorder
        self.recorder = GameRecorder()
        self.is_recording = False
        
        # UI elements
        self.buttons = []
        self.create_game_buttons()
        
        # Create fullscreen toggle button
        self.fullscreen_button = pygame.Rect(self.width - 200, self.height - 60, 180, 40)
        self.fullscreen_button_hover = False
        
        # Create record button
        self.record_button = pygame.Rect(20, self.height - 60, 180, 40)
        self.record_button_hover = False
        
        # Load background
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((20, 20, 40))
        
        # Try to load a font
        try:
            self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
            self.font_medium = pygame.font.SysFont("Arial", 32)
            self.font_small = pygame.font.SysFont("Arial", 24)
        except:
            self.font_large = None
            self.font_medium = None
            self.font_small = None
        
        # Set up colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.HIGHLIGHT = (100, 150, 255)
        self.BUTTON_COLOR = (50, 50, 80)
        self.HOVER_COLOR = (70, 70, 120)
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Load game manager
        self.game_manager = GameManager()
        self.games = self.game_manager.get_available_games()
        
        # UI elements
        self.buttons = []
        self.create_game_buttons()
        
        # Load background
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((20, 20, 40))
        
        # Try to load a font
        try:
            self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
            self.font_medium = pygame.font.SysFont("Arial", 32)
            self.font_small = pygame.font.SysFont("Arial", 24)
        except:
            self.font_large = None
            self.font_medium = None
            self.font_small = None
        
    def create_game_buttons(self):
        """Create buttons for each available game."""
        button_width, button_height = 280, 200
        margin = 30
        cols = 3
        
        # Calculate button size based on screen dimensions
        # Use a percentage of screen width for button width
        button_width = min(280, int(self.width * 0.25))
        button_height = int(button_width * 0.7)  # Maintain aspect ratio
        
        # Adjust margin based on screen size
        margin = int(self.width * 0.03)
        
        # Calculate number of columns based on screen width
        cols = max(2, min(5, self.width // (button_width + margin)))
        
        for i, game in enumerate(self.games):
            row = i // cols
            col = i % cols
            
            x = margin + col * (button_width + margin)
            y = 150 + row * (button_height + margin)
            
            self.buttons.append({
                'rect': pygame.Rect(x, y, button_width, button_height),
                'game': game,
                'name': game['name'],
                'thumbnail': game.get('thumbnail', None),
                'hover': False
            })
    
    def draw(self):
        """Draw the launcher interface."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw decorative elements
        pygame.draw.rect(self.screen, (30, 30, 60), (0, 0, self.width, 100))
        pygame.draw.line(self.screen, self.HIGHLIGHT, (0, 100), (self.width, 100), 3)
        
        # Draw title
        if self.font_large:
            title_surf = self.font_large.render("PYGAME ARCADE", True, self.WHITE)
            title_rect = title_surf.get_rect(center=(self.width // 2, 50))
            self.screen.blit(title_surf, title_rect)
        else:
            draw_text(self.screen, "PYGAME ARCADE", 64, self.WHITE, self.width // 2, 50)
        
        # Draw game buttons
        for button in self.buttons:
            # Draw button background with hover effect
            color = self.HOVER_COLOR if button['hover'] else self.BUTTON_COLOR
            pygame.draw.rect(self.screen, color, button['rect'], 0)
            pygame.draw.rect(self.screen, self.HIGHLIGHT, button['rect'], 3)
            
            # Draw game name
            if self.font_medium:
                name_surf = self.font_medium.render(button['name'], True, self.WHITE)
                name_rect = name_surf.get_rect(center=(button['rect'].centerx, button['rect'].centery - 20))
                self.screen.blit(name_surf, name_rect)
            else:
                draw_text(self.screen, button['name'], 32, self.WHITE, 
                         button['rect'].centerx, button['rect'].centery - 20)
            
            # Draw "Play" text
            if self.font_small:
                play_surf = self.font_small.render("Click to Play", True, self.WHITE)
                play_rect = play_surf.get_rect(center=(button['rect'].centerx, button['rect'].centery + 40))
                self.screen.blit(play_surf, play_rect)
            else:
                draw_text(self.screen, "Click to Play", 24, self.WHITE, 
                         button['rect'].centerx, button['rect'].centery + 40)
            
            # Draw thumbnail if available
            if button['thumbnail']:
                # Implementation would load and display the thumbnail
                pass
        
        # Draw fullscreen toggle button
        color = self.HOVER_COLOR if self.fullscreen_button_hover else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.fullscreen_button, 0)
        pygame.draw.rect(self.screen, self.HIGHLIGHT, self.fullscreen_button, 3)
        
        # Draw fullscreen button text
        button_text = "Exit Fullscreen" if self.is_fullscreen else "Enter Fullscreen"
        if self.font_small:
            fs_text = self.font_small.render(button_text, True, self.WHITE)
            fs_rect = fs_text.get_rect(center=self.fullscreen_button.center)
            self.screen.blit(fs_text, fs_rect)
        else:
            draw_text(self.screen, button_text, 24, self.WHITE, 
                     self.fullscreen_button.centerx, self.fullscreen_button.centery)
        
        # Draw record button
        color = self.RECORD_RED if self.is_recording else (self.HOVER_COLOR if self.record_button_hover else self.BUTTON_COLOR)
        pygame.draw.rect(self.screen, color, self.record_button, 0)
        pygame.draw.rect(self.screen, self.HIGHLIGHT, self.record_button, 3)
        
        # Draw record button text
        record_text = "Stop Recording" if self.is_recording else "Start Recording"
        if self.font_small:
            rec_text = self.font_small.render(record_text, True, self.WHITE)
            rec_rect = rec_text.get_rect(center=self.record_button.center)
            self.screen.blit(rec_text, rec_rect)
        else:
            draw_text(self.screen, record_text, 24, self.WHITE, 
                     self.record_button.centerx, self.record_button.centery)
        
        # Draw recording indicator if recording
        if self.is_recording:
            # Draw red recording circle
            pygame.draw.circle(self.screen, self.RECORD_RED, (30, 30), 10)
            
            if self.font_small:
                rec_ind = self.font_small.render("REC", True, self.RECORD_RED)
                self.screen.blit(rec_ind, (45, 20))
        
        # Draw footer
        if self.font_small:
            footer_surf = self.font_small.render("Press ESC to quit", True, self.WHITE)
            footer_rect = footer_surf.get_rect(center=(self.width // 2, self.height - 30))
            self.screen.blit(footer_surf, footer_rect)
        else:
            draw_text(self.screen, "Press ESC to quit", 24, self.WHITE, self.width // 2, self.height - 30)
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_f:
                    # Toggle fullscreen with F key
                    self.toggle_fullscreen()
                elif event.key == pygame.K_r:
                    # Toggle recording with R key
                    self.toggle_recording()
            
            if event.type == pygame.MOUSEMOTION:
                # Handle hover effects
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button['hover'] = button['rect'].collidepoint(mouse_pos)
                
                # Check fullscreen button hover
                self.fullscreen_button_hover = self.fullscreen_button.collidepoint(mouse_pos)
                
                # Check record button hover
                self.record_button_hover = self.record_button.collidepoint(mouse_pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check game buttons
                    for button in self.buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            self.launch_game(button['game'])
                    
                    # Check fullscreen button
                    if self.fullscreen_button.collidepoint(mouse_pos):
                        self.toggle_fullscreen()
                    
                    # Check record button
                    if self.record_button.collidepoint(mouse_pos):
                        self.toggle_recording()
        
        # Capture frame if recording
        if self.is_recording:
            self.recorder.capture_frame(self.screen)
        
        return True
        
    def toggle_recording(self):
        """Toggle video recording on/off."""
        if self.is_recording:
            self.recorder.stop_recording()
            self.is_recording = False
        else:
            self.recorder.start_recording(self.width, self.height)
            self.is_recording = True
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            from config import SCREEN_WIDTH, SCREEN_HEIGHT
            self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
            self.screen = pygame.display.set_mode((self.width, self.height))
            
        # Update config
        import config
        config.FULLSCREEN = self.is_fullscreen
        
        # Recreate buttons for new screen size
        self.buttons = []
        self.create_game_buttons()
        
        # Update button positions based on new screen dimensions
        self.fullscreen_button = pygame.Rect(self.width - 200, self.height - 60, 180, 40)
        self.record_button = pygame.Rect(20, self.height - 60, 180, 40)
        
        # Recreate background surface for new dimensions
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((20, 20, 40))
    
    def launch_game(self, game):
        """Launch the selected game."""
        print(f"Launching {game['name']}...")
        
        try:
            # Import the game module
            module_name = game['module']
            game_module = importlib.import_module(module_name)
            
            # Pass fullscreen state to the game
            if hasattr(game_module, 'main') and callable(game_module.main):
                # Prepare arguments
                kwargs = {}
                
                # Pass fullscreen parameter if the game accepts it
                try:
                    kwargs['fullscreen'] = self.is_fullscreen
                except:
                    pass
                
                # If recording, pass the recorder
                if self.is_recording:
                    try:
                        kwargs['recorder'] = self.recorder
                    except:
                        pass
                
                # Call the game's main function with appropriate arguments
                try:
                    score = game_module.main(**kwargs)
                except TypeError:
                    # If the game doesn't accept our parameters, call without them
                    score = game_module.main()
            
            # Reset display for launcher
            from config import SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN
            
            if self.is_fullscreen:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.width, self.height = self.screen.get_size()
            else:
                self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
                self.screen = pygame.display.set_mode((self.width, self.height))
                
            pygame.display.set_caption("Pygame Arcade Launcher")
            
            # Recreate buttons for new screen size
            self.buttons = []
            self.create_game_buttons()
            
            # Update button positions
            self.fullscreen_button = pygame.Rect(self.width - 200, self.height - 60, 180, 40)
            self.record_button = pygame.Rect(20, self.height - 60, 180, 40)
            
            print(f"Game '{game['name']}' finished with score: {score}")
            
        except Exception as e:
            print(f"Error launching game: {e}")
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(self.FPS)
