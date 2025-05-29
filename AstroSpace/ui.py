import pygame
from config import *

class Button:
    """Interactive button for UI screens"""
    
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        
        # Colors
        self.normal_color = (50, 50, 50)
        self.hover_color = (75, 75, 75)
        self.text_color = WHITE
        self.border_color = NEON_BLUE
        
        # State
        self.hovered = False
    
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        """Handle mouse click events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                return self.action
        return None
    
    def draw(self, surface):
        """Draw the button"""
        # Draw button background
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, width=2, border_radius=10)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class HealthBar:
    """Health bar for displaying player lives"""
    
    def __init__(self, x, y, width, height, max_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = max_value
        
        # Colors
        self.border_color = WHITE
        self.background_color = (50, 50, 50)
        self.health_color = GREEN
        self.low_health_color = RED
    
    def update(self, current_value):
        """Update the health bar with a new value"""
        # Smoothly transition to the new value
        if self.current_value > current_value:
            self.current_value = max(self.current_value - 0.1, current_value)
        elif self.current_value < current_value:
            self.current_value = min(self.current_value + 0.1, current_value)
    
    def draw(self, surface):
        """Draw the health bar"""
        # Draw background
        pygame.draw.rect(surface, self.background_color, self.rect)
        
        # Draw health
        health_width = int(self.rect.width * (self.current_value / self.max_value))
        health_rect = pygame.Rect(self.rect.x, self.rect.y, health_width, self.rect.height)
        
        # Change color based on health percentage
        health_percent = self.current_value / self.max_value
        if health_percent > 0.6:
            color = self.health_color
        elif health_percent > 0.3:
            color = YELLOW
        else:
            color = self.low_health_color
        
        pygame.draw.rect(surface, color, health_rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, width=2)

class ScoreDisplay:
    """Display for the player's score"""
    
    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.font = font
        self.score = 0
        self.displayed_score = 0
        self.transition_speed = 5  # How fast the score changes visually
    
    def update(self, score):
        """Update the score display"""
        self.score = score
        
        # Smoothly transition to the new score
        if self.displayed_score < self.score:
            self.displayed_score = min(self.displayed_score + self.transition_speed, self.score)
        elif self.displayed_score > self.score:
            self.displayed_score = max(self.displayed_score - self.transition_speed, self.score)
    
    def reset(self):
        """Reset the displayed score to match the actual score immediately"""
        self.displayed_score = self.score
    
    def draw(self, surface):
        """Draw the score display"""
        score_text = f"SCORE: {self.displayed_score}"
        score_surf = self.font.render(score_text, True, NEON_BLUE)
        
        # Add drop shadow
        shadow_surf = self.font.render(score_text, True, (20, 20, 50))
        surface.blit(shadow_surf, (self.x + 2, self.y + 2))
        surface.blit(score_surf, (self.x, self.y))

class LivesDisplay:
    """Display for the player's remaining lives"""
    
    def __init__(self, x, y, font, ship_image=None):
        self.x = x
        self.y = y
        self.font = font
        self.ship_image = ship_image
        self.lives = 3
    
    def update(self, lives):
        """Update the lives display"""
        self.lives = lives
    
    def draw(self, surface):
        """Draw the lives display"""
        if self.ship_image:
            # Draw ship icons
            for i in range(self.lives):
                # Scale down the ship image
                scaled_ship = pygame.transform.scale(self.ship_image, (25, 25))
                surface.blit(scaled_ship, (self.x + i * 30, self.y))
        else:
            # Draw text
            lives_text = f"LIVES: {self.lives}"
            lives_surf = self.font.render(lives_text, True, WHITE)
            surface.blit(lives_surf, (self.x, self.y))

class PowerupIndicator:
    """Display for active powerups"""
    
    def __init__(self, x, y, font):
        self.x = x
        self.y = y
        self.font = font
        self.active_powerups = {}
    
    def update(self, player):
        """Update the powerup indicators"""
        current_time = pygame.time.get_ticks()
        self.active_powerups = {}
        
        # Check each powerup
        if player.double_shot and current_time < player.powerup_end_times['double']:
            remaining = (player.powerup_end_times['double'] - current_time) / 1000
            self.active_powerups['Double Shot'] = remaining
        
        if player.invincible and current_time < player.powerup_end_times['shield']:
            remaining = (player.powerup_end_times['shield'] - current_time) / 1000
            self.active_powerups['Shield'] = remaining
        
        if player.speed > PLAYER_SPEED and current_time < player.powerup_end_times['speed']:
            remaining = (player.powerup_end_times['speed'] - current_time) / 1000
            self.active_powerups['Speed Boost'] = remaining
    
    def draw(self, surface):
        """Draw the powerup indicators"""
        y_offset = 0
        for name, remaining in self.active_powerups.items():
            text = f"{name}: {remaining:.1f}s"
            text_surf = self.font.render(text, True, WHITE)
            surface.blit(text_surf, (self.x, self.y + y_offset))
            y_offset += 25
