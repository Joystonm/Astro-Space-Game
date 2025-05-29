import pygame
from bullet import Bullet
from config import *

class Player:
    def __init__(self, assets):
        self.image = assets['player_ship']
        self.rect = self.image.get_rect()
        
        # Position the player at the bottom center of the screen
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        
        # Movement attributes
        self.speed = PLAYER_SPEED
        self.dx = 0
        self.dy = 0
        
        # Shooting attributes
        self.last_shot = 0
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.bullets = []
        
        # Player stats
        self.lives = PLAYER_LIVES
        self.score = 0
        
        # Power-up states
        self.double_shot = False
        self.invincible = False
        self.powerup_end_times = {
            'double': 0,
            'shield': 0,
            'speed': 0
        }
        
        # Invincibility after hit
        self.hit_invincibility_end = 0
        
        # Animation
        self.explosion_anim = assets['explosion_anim']
        self.exploding = False
        self.explosion_frame = 0
        
        # Sound effects
        self.shoot_sound = assets['shoot_sound']
        self.explosion_sound = assets['explosion_sound']
    
    def handle_input(self, event):
        # Key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.dx = -self.speed
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.dx = self.speed
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.dy = -self.speed
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.dy = self.speed
            # We'll handle shooting in the main game loop with get_pressed()
        
        # Key release events
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.dx < 0:
                self.dx = 0
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.dx > 0:
                self.dx = 0
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.dy < 0:
                self.dy = 0
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.dy > 0:
                self.dy = 0
    
    def update(self):
        # Check for power-up expirations
        current_time = pygame.time.get_ticks()
        
        if self.double_shot and current_time > self.powerup_end_times['double']:
            self.double_shot = False
        
        if self.invincible and current_time > self.powerup_end_times['shield'] and current_time > self.hit_invincibility_end:
            self.invincible = False
        
        if self.speed > PLAYER_SPEED and current_time > self.powerup_end_times['speed']:
            self.speed = PLAYER_SPEED
        
        # Update position
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def shoot(self):
        """
        Attempt to fire a bullet. Returns a list of bullets fired or an empty list if on cooldown.
        """
        # Check if enough time has passed since the last shot
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            bullets_fired = []
            
            if self.double_shot:
                # Create two bullets side by side
                bullet1 = Bullet(self.rect.left + 10, self.rect.top, -1)
                bullet2 = Bullet(self.rect.right - 10, self.rect.top, -1)
                bullets_fired.extend([bullet1, bullet2])
            else:
                # Create a single bullet at the player's position
                bullet = Bullet(self.rect.centerx, self.rect.top, -1)
                bullets_fired.append(bullet)
            
            # Play shoot sound
            self.shoot_sound.play()
            
            return bullets_fired
        
        return []
    
    def hit(self):
        """Handle player being hit by an enemy"""
        if not self.invincible:
            self.lives -= 1
            self.explosion_sound.play()
            
            # Temporary invincibility after being hit
            self.invincible = True
            self.hit_invincibility_end = pygame.time.get_ticks() + INVINCIBILITY_DURATION
            
            return True
        return False
    
    def is_dead(self):
        """Check if the player is dead (no lives left)"""
        return self.lives <= 0
    
    def draw(self, surface):
        # If invincible, make the player blink
        if self.invincible:
            if pygame.time.get_ticks() % 200 < 100:
                surface.blit(self.image, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        # Draw shield effect if active
        if self.invincible and pygame.time.get_ticks() <= self.powerup_end_times['shield']:
            pygame.draw.circle(surface, BLUE, self.rect.center, self.rect.width // 2 + 5, 2)
