import pygame
import random
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (25, 25, 112)
LIGHT_BLUE = (135, 206, 235)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
RED = (220, 20, 60)
DARK_RED = (139, 0, 0)
GREEN = (50, 205, 50)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
PURPLE = (138, 43, 226)

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.speed = 6
        self.rect = pygame.Rect(x + 10, y + 10, self.width - 20, self.height - 20)
        self.flame_offset = 0
    
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            self.rect.x = self.x + 10
    
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.rect.x = self.x + 10
    
    def draw(self, screen):
        center_x = self.x + self.width // 2
        
        # Draw rocket flames (animated)
        self.flame_offset = (self.flame_offset + 1) % 10
        flame_height = 15 + self.flame_offset // 2
        flame_points = [
            (center_x - 8, self.y + self.height),
            (center_x, self.y + self.height + flame_height),
            (center_x + 8, self.y + self.height)
        ]
        pygame.draw.polygon(screen, ORANGE, flame_points)
        
        # Inner flame
        inner_flame_points = [
            (center_x - 4, self.y + self.height),
            (center_x, self.y + self.height + flame_height - 5),
            (center_x + 4, self.y + self.height)
        ]
        pygame.draw.polygon(screen, YELLOW, inner_flame_points)
        
        # Draw rocket body (main cylinder)
        body_rect = pygame.Rect(self.x + 8, self.y + 20, self.width - 16, self.height - 30)
        pygame.draw.rect(screen, SILVER, body_rect)
        pygame.draw.rect(screen, GRAY, body_rect, 2)
        
        # Draw rocket nose cone
        nose_points = [
            (center_x, self.y),
            (self.x + 8, self.y + 20),
            (self.x + self.width - 8, self.y + 20)
        ]
        pygame.draw.polygon(screen, LIGHT_GRAY, nose_points)
        pygame.draw.polygon(screen, GRAY, nose_points, 2)
        
        # Draw rocket fins
        left_fin = [
            (self.x + 8, self.y + 50),
            (self.x, self.y + 70),
            (self.x + 8, self.y + 70)
        ]
        right_fin = [
            (self.x + self.width - 8, self.y + 50),
            (self.x + self.width, self.y + 70),
            (self.x + self.width - 8, self.y + 70)
        ]
        pygame.draw.polygon(screen, DARK_BLUE, left_fin)
        pygame.draw.polygon(screen, DARK_BLUE, right_fin)
        pygame.draw.polygon(screen, BLACK, left_fin, 2)
        pygame.draw.polygon(screen, BLACK, right_fin, 2)
        
        # Draw rocket details
        # Window
        pygame.draw.circle(screen, LIGHT_BLUE, (center_x, self.y + 30), 6)
        pygame.draw.circle(screen, DARK_BLUE, (center_x, self.y + 30), 6, 2)
        
        # Body stripes
        for i in range(3):
            stripe_y = self.y + 40 + i * 8
            pygame.draw.line(screen, DARK_BLUE, (self.x + 10, stripe_y), (self.x + self.width - 10, stripe_y), 2)

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 50
        self.speed = 3
        self.rect = pygame.Rect(x + 5, y + 5, self.width - 10, self.height - 10)
        self.rotation = 0
        self.fuse_spark = 0
    
    def fall(self):
        self.y += self.speed
        self.rect.y = self.y + 5
        self.rotation += 2
        self.fuse_spark = (self.fuse_spark + 1) % 20
    
    def draw(self, screen):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # Draw bomb shadow
        shadow_offset = 3
        shadow_rect = pygame.Rect(self.x + shadow_offset, self.y + shadow_offset, self.width, self.height - 10)
        pygame.draw.ellipse(screen, (50, 50, 50), shadow_rect)
        
        # Draw main bomb body (sphere)
        bomb_rect = pygame.Rect(self.x, self.y + 10, self.width, self.height - 10)
        pygame.draw.ellipse(screen, BLACK, bomb_rect)
        pygame.draw.ellipse(screen, DARK_RED, bomb_rect, 3)
        
        # Draw bomb highlight
        highlight_rect = pygame.Rect(self.x + 8, self.y + 15, self.width - 20, self.height - 25)
        pygame.draw.ellipse(screen, GRAY, highlight_rect)
        
        # Draw fuse
        fuse_length = 15
        fuse_x = center_x + math.cos(math.radians(self.rotation)) * 3
        fuse_y = self.y + 5
        pygame.draw.line(screen, (139, 69, 19), (center_x, self.y + 10), (fuse_x, fuse_y - fuse_length), 4)
        
        # Draw sparking fuse tip
        if self.fuse_spark < 10:
            spark_colors = [YELLOW, ORANGE, RED]
            spark_color = spark_colors[self.fuse_spark % 3]
            pygame.draw.circle(screen, spark_color, (int(fuse_x), int(fuse_y - fuse_length)), 3)
            
            # Draw small sparks around fuse
            for i in range(3):
                spark_x = fuse_x + random.randint(-5, 5)
                spark_y = fuse_y - fuse_length + random.randint(-3, 3)
                pygame.draw.circle(screen, spark_color, (int(spark_x), int(spark_y)), 1)
        
        # Draw "BOMB" text on the bomb
        font = pygame.font.Font(None, 16)
        text = font.render("BOMB", True, WHITE)
        text_rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, text_rect)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 60
        self.particles = []
        self.lifetime = 30
        
        # Create explosion particles
        for _ in range(15):
            particle = {
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(-10, 10),
                'vx': random.randint(-8, 8),
                'vy': random.randint(-8, 8),
                'color': random.choice([RED, ORANGE, YELLOW]),
                'size': random.randint(3, 8)
            }
            self.particles.append(particle)
    
    def update(self):
        self.radius = min(self.radius + 3, self.max_radius)
        self.lifetime -= 1
        
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # gravity
            particle['size'] = max(1, particle['size'] - 0.2)
    
    def draw(self, screen):
        if self.lifetime > 0:
            # Draw main explosion circle
            alpha = max(0, self.lifetime * 8)
            explosion_surface = pygame.Surface((self.radius * 2, self.radius * 2))
            explosion_surface.set_alpha(alpha)
            pygame.draw.circle(explosion_surface, ORANGE, (self.radius, self.radius), self.radius)
            screen.blit(explosion_surface, (self.x - self.radius, self.y - self.radius))
            
            # Draw particles
            for particle in self.particles:
                if particle['size'] > 1:
                    pygame.draw.circle(screen, particle['color'], 
                                     (int(particle['x']), int(particle['y'])), 
                                     int(particle['size']))
    
    def is_finished(self):
        return self.lifetime <= 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🚀 Rocket vs Bomb 💣")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.rocket = Rocket(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 100)
        self.bombs = []
        self.explosions = []
        self.bomb_spawn_timer = 0
        self.bomb_spawn_delay = 80  # frames
        
        # Game state
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.level = 1
        
        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 64)
        self.title_font = pygame.font.Font(None, 48)
        
        # Background stars
        self.stars = []
        for _ in range(100):
            star = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2),
                'brightness': random.randint(100, 255)
            }
            self.stars.append(star)
    
    def spawn_bomb(self):
        x = random.randint(0, SCREEN_WIDTH - 40)
        bomb = Bomb(x, -50)
        self.bombs.append(bomb)
    
    def draw_background(self):
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(25 * (1 - color_ratio))
            g = int(25 * (1 - color_ratio))
            b = int(112 * (1 - color_ratio) + 25 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw moving stars
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
            
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (int(star['x']), int(star['y'])), 1)
    
    def draw_ui(self):
        # Draw HUD background
        hud_surface = pygame.Surface((SCREEN_WIDTH, 60))
        hud_surface.set_alpha(180)
        hud_surface.fill(BLACK)
        self.screen.blit(hud_surface, (0, 0))
        
        # Score
        score_text = self.font.render(f"SCORE: {self.score:06d}", True, GOLD)
        self.screen.blit(score_text, (20, 15))
        
        # Lives
        lives_text = self.font.render(f"LIVES: ", True, WHITE)
        self.screen.blit(lives_text, (200, 15))
        for i in range(self.lives):
            heart_x = 280 + i * 25
            pygame.draw.polygon(self.screen, RED, [
                (heart_x, 25), (heart_x - 8, 15), (heart_x - 8, 10),
                (heart_x - 4, 6), (heart_x, 10), (heart_x + 4, 6),
                (heart_x + 8, 10), (heart_x + 8, 15)
            ])
        
        # Level
        level_text = self.font.render(f"LEVEL: {self.level}", True, LIGHT_BLUE)
        self.screen.blit(level_text, (400, 15))
        
        # Instructions
        if self.score < 50:  # Show instructions for new players
            instruction_text = self.font.render("← → or A/D to move | ESC to quit | P to pause", True, LIGHT_GRAY)
            self.screen.blit(instruction_text, (20, SCREEN_HEIGHT - 25))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if not self.game_over and not self.paused:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rocket.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rocket.move_right()
        
        return True
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        # Update level based on score
        self.level = (self.score // 200) + 1
        
        # Spawn bombs
        self.bomb_spawn_timer += 1
        spawn_delay = max(30, self.bomb_spawn_delay - (self.level - 1) * 5)
        if self.bomb_spawn_timer >= spawn_delay:
            self.spawn_bomb()
            self.bomb_spawn_timer = 0
        
        # Update bombs
        for bomb in self.bombs[:]:
            bomb.fall()
            
            # Remove bombs that have fallen off screen
            if bomb.y > SCREEN_HEIGHT:
                self.bombs.remove(bomb)
                self.score += 10  # Score for avoiding bomb
            
            # Check collision with rocket
            elif bomb.rect.colliderect(self.rocket.rect):
                # Create explosion
                explosion = Explosion(bomb.x + bomb.width // 2, bomb.y + bomb.height // 2)
                self.explosions.append(explosion)
                
                self.bombs.remove(bomb)
                self.lives -= 1
                
                if self.lives <= 0:
                    self.game_over = True
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        # Increase bomb speed based on level
        for bomb in self.bombs:
            bomb.speed = 3 + (self.level - 1) * 0.5
    
    def draw(self):
        # Draw background
        self.draw_background()
        
        if self.paused:
            # Draw pause screen
            pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            pause_surface.set_alpha(128)
            pause_surface.fill(BLACK)
            self.screen.blit(pause_surface, (0, 0))
            
            pause_text = self.big_font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, pause_rect)
            
            resume_text = self.font.render("Press P to resume", True, LIGHT_GRAY)
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(resume_text, resume_rect)
        
        elif not self.game_over:
            # Draw game objects
            self.rocket.draw(self.screen)
            for bomb in self.bombs:
                bomb.draw(self.screen)
            for explosion in self.explosions:
                explosion.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
        
        else:
            # Draw game over screen
            game_over_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            game_over_surface.set_alpha(200)
            game_over_surface.fill(BLACK)
            self.screen.blit(game_over_surface, (0, 0))
            
            # Game over text with glow effect
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                shadow_text = self.big_font.render("GAME OVER", True, DARK_RED)
                shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + offset[0], SCREEN_HEIGHT // 2 - 50 + offset[1]))
                self.screen.blit(shadow_text, shadow_rect)
            
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, game_over_rect)
            
            # Final stats
            final_score_text = self.title_font.render(f"Final Score: {self.score:06d}", True, GOLD)
            final_level_text = self.font.render(f"Level Reached: {self.level}", True, LIGHT_BLUE)
            restart_text = self.font.render("Press R to Restart or ESC to Quit", True, WHITE)
            
            score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            level_rect = final_level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            
            self.screen.blit(final_score_text, score_rect)
            self.screen.blit(final_level_text, level_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def restart_game(self):
        self.rocket = Rocket(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 100)
        self.bombs = []
        self.explosions = []
        self.bomb_spawn_timer = 0
        self.bomb_spawn_delay = 80
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.paused = False
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        return self.score

def main():
    """Main function to start the Rocket vs Bomb game"""
    try:
        game = Game()
        final_score = game.run()
        pygame.quit()
        return final_score
    except Exception as e:
        print(f"Error running Rocket vs Bomb: {e}")
        pygame.quit()
        return 0

if __name__ == "__main__":
    main()
