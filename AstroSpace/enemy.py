import pygame
import random
from config import *

class Enemy:
    def __init__(self, assets):
        self.image = assets['enemy_ship']
        self.original_image = self.image  # Store original for rotation
        self.rect = self.image.get_rect()
        
        # Position the enemy at a random location at the top of the screen
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        
        # Movement attributes
        self.speed_x = random.randint(-1, 1)
        self.speed_y = random.randint(1, 3)
        
        # Rotation for tumbling effect
        self.angle = 0
        self.rotation_speed = random.randint(-3, 3)
        if self.rotation_speed == 0:
            self.rotation_speed = 1
        
        # Sound effects
        self.explosion_sound = assets['explosion_sound']
    
    def update(self):
        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Randomly change horizontal direction occasionally
        if random.random() < 0.01:
            self.speed_x = random.randint(-2, 2)
        
        # Keep enemy within screen bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = abs(self.speed_x)
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x = -abs(self.speed_x)
        
        # Rotate the asteroid for tumbling effect
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        # Keep the center position the same after rotation
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
