import pygame
from config import *

class Button:
    """Interactive button for menus"""
    
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        
        # Colors
        self.normal_color = (50, 50, 100)
        self.hover_color = (70, 70, 150)
        self.click_color = (100, 100, 200)
        self.text_color = WHITE
        
        # State
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        """Handle mouse events on the button"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.clicked = True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.clicked and self.hovered:
                self.clicked = False
                return self.action
            self.clicked = False
        
        return None
    
    def draw(self, surface):
        """Draw the button"""
        # Determine color based on state
        if self.clicked:
            color = self.click_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.normal_color
        
        # Draw button background
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        # Draw button border
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=10)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class HealthBar:
    """Health bar for the player"""
    
    def __init__(self, x, y, width, height, max_health):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = max_health
        self.current_health = max_health
        
        # Colors
        self.border_color = WHITE
        self.background_color = (50, 50, 50)
        self.health_color = GREEN
        self.low_health_color = RED
    
    def update(self, health):
        """Update the health bar"""
        self.current_health = health
    
    def draw(self, surface):
        """Draw the health bar"""
        # Draw background
        pygame.draw.rect(surface, self.background_color, self.rect)
        
        # Draw health level
        health_percent = self.current_health / self.max_health
        health_width = int(self.rect.width * health_percent)
        health_rect = pygame.Rect(self.rect.x, self.rect.y, health_width, self.rect.height)
        
        # Change color based on health percentage
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
        # Format score with commas for better readability
        formatted_score = f"{int(self.displayed_score):,}"
        score_text = f"SCORE: {formatted_score}"
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
        for powerup, remaining in self.active_powerups.items():
            text = f"{powerup}: {remaining:.1f}s"
            text_surf = self.font.render(text, True, WHITE)
            surface.blit(text_surf, (self.x, self.y + y_offset))
            y_offset += 25

class EnergyBar:
    """Energy bar for the Energy Blast mechanic"""
    
    def __init__(self, x, y, width, height, max_energy):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_energy = max_energy
        self.current_energy = 0
        self.is_charged = False
        self.glow_effect = 0
        
        # Colors
        self.border_color = WHITE
        self.background_color = (50, 50, 50)
        self.energy_color = NEON_BLUE
        self.charged_color = (100, 200, 255)
    
    def add_energy(self, amount=1):
        """Add energy to the bar"""
        self.current_energy = min(self.current_energy + amount, self.max_energy)
        if self.current_energy >= self.max_energy:
            self.is_charged = True
    
    def reset(self):
        """Reset energy after using blast"""
        self.current_energy = 0
        self.is_charged = False
    
    def draw(self, surface):
        """Draw the energy bar"""
        # Draw background
        pygame.draw.rect(surface, self.background_color, self.rect)
        
        # Draw energy level
        energy_width = int(self.rect.width * (self.current_energy / self.max_energy))
        energy_rect = pygame.Rect(self.rect.x, self.rect.y, energy_width, self.rect.height)
        
        # Add glow effect when fully charged
        if self.is_charged:
            self.glow_effect = (self.glow_effect + 1) % 30
            glow_intensity = abs(15 - self.glow_effect) / 15
            energy_color = (
                100 + int(155 * glow_intensity), 
                150 + int(105 * glow_intensity), 
                255
            )
            pygame.draw.rect(surface, energy_color, energy_rect)
        else:
            pygame.draw.rect(surface, self.energy_color, energy_rect)
        
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, width=2)
        
        # Draw energy text
        font = pygame.font.Font(MAIN_FONT, 14)
        energy_text = font.render(f"ENERGY: {self.current_energy}/{self.max_energy}", True, WHITE)
        text_rect = energy_text.get_rect(center=(self.rect.centerx, self.rect.centery))
        surface.blit(energy_text, text_rect)
