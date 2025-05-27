#!/usr/bin/env python3
"""
Car Racing Game
A top-down racing game where you avoid obstacles.
"""
import pygame
import sys
import os
import random

# Add parent directory to path so we can import from core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from core.utils import load_image, draw_text

class CarRacing:
    """Main Car Racing game class."""
    
    def __init__(self, fullscreen=False):
        """Initialize the game."""
        # Initialize display
        self.width, self.height = 1024, 768
        
        # Set up display mode based on fullscreen parameter
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
            self.is_fullscreen = True
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.is_fullscreen = False
            
        pygame.display.set_caption("Car Racing")
        
        # Set up colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.GRAY = (100, 100, 100)
        self.YELLOW = (255, 255, 0)
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Game state
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.running = True
        self.speed = 5
        self.max_speed = 15
        self.acceleration = 0.1
        self.road_pos = 0
        
        # Load assets
        self.load_assets()
        
        # Initialize game objects
        self.init_game_objects()
        
        # Load font
        try:
            self.font = pygame.font.SysFont("Arial", 32)
            self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 24)
        except:
            self.font = None
            self.font_large = None
            self.font_small = None
    
    def load_assets(self):
        """Load game assets like images and sounds."""
        self.assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        
        # Create player car
        self.player_car = pygame.Surface((60, 100), pygame.SRCALPHA)
        self.player_car.fill((0, 0, 255))  # Blue car
        pygame.draw.rect(self.player_car, (0, 0, 150), (5, 5, 50, 90))  # Darker blue body
        pygame.draw.rect(self.player_car, (200, 200, 200), (10, 15, 40, 30))  # Windshield
        pygame.draw.rect(self.player_car, (0, 0, 0), (5, 0, 50, 10))  # Front bumper
        pygame.draw.rect(self.player_car, (0, 0, 0), (5, 90, 50, 10))  # Rear bumper
        pygame.draw.rect(self.player_car, (0, 0, 0), (5, 25, 10, 20))  # Left window
        pygame.draw.rect(self.player_car, (0, 0, 0), (45, 25, 10, 20))  # Right window
        
        # Create obstacle cars
        self.obstacle_cars = []
        
        # Red car
        red_car = pygame.Surface((60, 100), pygame.SRCALPHA)
        red_car.fill((200, 0, 0))  # Red car
        pygame.draw.rect(red_car, (150, 0, 0), (5, 5, 50, 90))  # Darker red body
        pygame.draw.rect(red_car, (200, 200, 200), (10, 15, 40, 30))  # Windshield
        pygame.draw.rect(red_car, (0, 0, 0), (5, 0, 50, 10))  # Front bumper
        pygame.draw.rect(red_car, (0, 0, 0), (5, 90, 50, 10))  # Rear bumper
        self.obstacle_cars.append(red_car)
        
        # Green car
        green_car = pygame.Surface((60, 100), pygame.SRCALPHA)
        green_car.fill((0, 200, 0))  # Green car
        pygame.draw.rect(green_car, (0, 150, 0), (5, 5, 50, 90))  # Darker green body
        pygame.draw.rect(green_car, (200, 200, 200), (10, 15, 40, 30))  # Windshield
        pygame.draw.rect(green_car, (0, 0, 0), (5, 0, 50, 10))  # Front bumper
        pygame.draw.rect(green_car, (0, 0, 0), (5, 90, 50, 10))  # Rear bumper
        self.obstacle_cars.append(green_car)
        
        # Yellow car
        yellow_car = pygame.Surface((60, 100), pygame.SRCALPHA)
        yellow_car.fill((200, 200, 0))  # Yellow car
        pygame.draw.rect(yellow_car, (150, 150, 0), (5, 5, 50, 90))  # Darker yellow body
        pygame.draw.rect(yellow_car, (200, 200, 200), (10, 15, 40, 30))  # Windshield
        pygame.draw.rect(yellow_car, (0, 0, 0), (5, 0, 50, 10))  # Front bumper
        pygame.draw.rect(yellow_car, (0, 0, 0), (5, 90, 50, 10))  # Rear bumper
        self.obstacle_cars.append(yellow_car)
    
    def init_game_objects(self):
        """Initialize game objects like player car and obstacles."""
        # Road width proportional to screen width
        self.road_width = min(400, int(self.width * 0.4))
        
        # Center the road in the screen
        self.road_left = (self.width - self.road_width) // 2
        self.road_right = self.road_left + self.road_width
        
        # Player car - centered on the road
        self.player_x = self.width // 2 - 30
        self.player_y = self.height - 150
        
        # Lane markers
        self.lane_marker_width = 10
        self.lane_marker_height = 50
        self.lane_marker_gap = 40
        self.lane_markers = []
        
        # Create initial lane markers
        for y in range(-self.lane_marker_height, self.height, self.lane_marker_height + self.lane_marker_gap):
            self.lane_markers.append(y)
        
        # Obstacles
        self.obstacles = []
        self.obstacle_speed = 5
        self.obstacle_frequency = 1500  # milliseconds
        self.last_obstacle_time = pygame.time.get_ticks()
    
    def create_obstacle(self):
        """Create a new obstacle car."""
        lanes = 3
        lane_width = self.road_width // lanes
        lane = random.randint(0, lanes - 1)
        
        x = self.road_left + lane * lane_width + (lane_width - 60) // 2
        y = -150  # Start above the screen
        
        car_type = random.randint(0, len(self.obstacle_cars) - 1)
        
        self.obstacles.append({
            'x': x,
            'y': y,
            'type': car_type,
            'width': 60,
            'height': 100
        })
    
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                
                # Toggle fullscreen with F key
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()
        
        # Continuous movement
        if not self.game_over:
            keys = pygame.key.get_pressed()
            
            # Horizontal movement
            move_speed = 8 * (self.width / 1024)  # Scale movement speed based on screen width
            
            if keys[pygame.K_LEFT]:
                self.player_x -= move_speed
                if self.player_x < self.road_left + 10:
                    self.player_x = self.road_left + 10
            if keys[pygame.K_RIGHT]:
                self.player_x += move_speed
                if self.player_x > self.road_right - 70:
                    self.player_x = self.road_right - 70
            
            # Speed control
            if keys[pygame.K_UP]:
                self.speed += self.acceleration
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
            elif keys[pygame.K_DOWN]:
                self.speed -= self.acceleration * 2
                if self.speed < 1:
                    self.speed = 1
            else:
                # Gradually return to normal speed
                if self.speed > 5:
                    self.speed -= self.acceleration / 2
                elif self.speed < 5:
                    self.speed += self.acceleration / 2
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            self.width, self.height = 1024, 768
            self.screen = pygame.display.set_mode((self.width, self.height))
        
        # Recalculate game object positions for the new screen size
        self.reset_game_layout()
    
    def reset_game_layout(self):
        """Reset the game layout based on current screen dimensions."""
        # Recenter the road - make road width proportional to screen width
        self.road_width = min(400, int(self.width * 0.4))
        self.road_left = (self.width - self.road_width) // 2
        self.road_right = self.road_left + self.road_width
        
        # Recenter the player
        self.player_x = self.width // 2 - 30
        self.player_y = self.height - 150
        
        # Reset lane markers
        self.lane_markers = []
        for y in range(-self.lane_marker_height, self.height, self.lane_marker_height + self.lane_marker_gap):
            self.lane_markers.append(y)
    
    def update(self):
        """Update game state."""
        if self.game_over:
            return
        
        # Update score
        self.score += int(self.speed)
        
        # Update road position for scrolling effect
        self.road_pos += self.speed
        if self.road_pos >= self.lane_marker_height + self.lane_marker_gap:
            self.road_pos = 0
            self.lane_markers.append(-self.lane_marker_height)
        
        # Update lane markers
        for i in range(len(self.lane_markers)):
            self.lane_markers[i] += self.speed
        
        # Remove lane markers that are off screen
        self.lane_markers = [y for y in self.lane_markers if y < self.height]
        
        # Create new obstacles
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.obstacle_frequency:
            self.create_obstacle()
            self.last_obstacle_time = current_time
            
            # Decrease obstacle frequency as score increases
            self.obstacle_frequency = max(500, 1500 - (self.score // 5000) * 100)
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle['y'] += self.obstacle_speed
            
            # Remove obstacles that are off screen
            if obstacle['y'] > self.height:
                self.obstacles.remove(obstacle)
        
        # Check for collisions
        self.check_collisions()
    
    def check_collisions(self):
        """Check for collisions between player car and obstacles."""
        player_rect = pygame.Rect(self.player_x, self.player_y, 60, 100)
        
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
            
            if player_rect.colliderect(obstacle_rect):
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                break
    
    def draw(self):
        """Draw the game state."""
        # Clear screen
        self.screen.fill(self.GREEN)  # Green for grass
        
        # Draw road
        pygame.draw.rect(self.screen, self.GRAY, 
                        (self.road_left, 0, self.road_width, self.height))
        
        # Draw lane dividers
        for y in self.lane_markers:
            pygame.draw.rect(self.screen, self.YELLOW, 
                            (self.width // 2 - self.lane_marker_width // 2, 
                             y, self.lane_marker_width, self.lane_marker_height))
        
        # Draw obstacles
        for obstacle in self.obstacles:
            self.screen.blit(self.obstacle_cars[obstacle['type']], (obstacle['x'], obstacle['y']))
        
        # Draw player car
        self.screen.blit(self.player_car, (self.player_x, self.player_y))
        
        # Draw UI panel
        pygame.draw.rect(self.screen, (30, 30, 50), (0, 0, self.width, 50))
        pygame.draw.line(self.screen, self.WHITE, (0, 50), (self.width, 50), 2)
        
        # Draw score
        if self.font:
            score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
            self.screen.blit(score_text, (20, 10))
            
            speed_text = self.font.render(f"Speed: {int(self.speed * 10)} km/h", True, self.WHITE)
            self.screen.blit(speed_text, (self.width // 2 - 80, 10))
            
            high_score_text = self.font.render(f"High Score: {self.high_score}", True, self.WHITE)
            self.screen.blit(high_score_text, (self.width - 250, 10))
        else:
            draw_text(self.screen, f"Score: {self.score}", 32, self.WHITE, 100, 25, align="left")
            draw_text(self.screen, f"Speed: {int(self.speed * 10)} km/h", 32, self.WHITE, self.width // 2, 25)
            draw_text(self.screen, f"High Score: {self.high_score}", 32, self.WHITE, self.width - 150, 25, align="right")
        
        # Draw game over message
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            if self.font_large:
                game_over_text = self.font_large.render("GAME OVER", True, self.RED)
                self.screen.blit(game_over_text, 
                                game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50)))
                
                score_text = self.font.render(f"Final Score: {self.score}", True, self.WHITE)
                self.screen.blit(score_text, 
                                score_text.get_rect(center=(self.width // 2, self.height // 2 + 20)))
                
                restart_text = self.font.render("Press R to Restart or ESC to Exit", True, self.WHITE)
                self.screen.blit(restart_text, 
                                restart_text.get_rect(center=(self.width // 2, self.height // 2 + 70)))
            else:
                draw_text(self.screen, "GAME OVER", 64, self.RED, self.width // 2, self.height // 2 - 50)
                draw_text(self.screen, f"Final Score: {self.score}", 32, self.WHITE, 
                         self.width // 2, self.height // 2 + 20)
                draw_text(self.screen, "Press R to Restart or ESC to Exit", 32, self.WHITE, 
                         self.width // 2, self.height // 2 + 70)
        
        # Update display
        pygame.display.flip()
    
    def reset_game(self):
        """Reset the game state to start a new game."""
        self.score = 0
        self.game_over = False
        self.speed = 5
        
        # Reset game layout based on current screen dimensions
        self.reset_game_layout()
        
        # Reset obstacles and game state
        self.obstacles = []
        self.obstacle_frequency = 1500
    
    def run(self, recorder=None):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            # Capture frame if recording
            if recorder and hasattr(recorder, 'capture_frame'):
                recorder.capture_frame(self.screen)
                
            self.clock.tick(self.FPS)
        
        return self.score

def main(fullscreen=False, recorder=None):
    """Initialize and run the game."""
    # Initialize pygame if not already done
    if not pygame.get_init():
        pygame.init()
    
    # Create and run the game
    game = CarRacing(fullscreen=fullscreen)
    
    # Use the game's run method instead of custom loop
    score = game.run(recorder)
    
    # Return to launcher without quitting pygame
    return score

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
