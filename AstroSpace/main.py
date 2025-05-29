#!/usr/bin/env python3
import pygame
import sys
import random
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp, spawn_random_powerup
from ui import Button, HealthBar, ScoreDisplay, LivesDisplay, PowerupIndicator
from config import *
from utils import load_assets, check_collisions, create_floating_text, update_floating_texts, draw_floating_texts

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Astro Space Game")
        
        # Set up the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Load assets
        self.assets = load_assets()
        
        # Game state
        self.state = STATE_SPLASH
        self.splash_start_time = pygame.time.get_ticks()
        
        # Initialize game objects
        self.reset_game()
        
        # UI elements
        self.init_ui()
        
        # Background scrolling
        self.bg_y = 0
        
        # Floating text effects
        self.floating_texts = []
        
        # Start background music
        self.assets['background_music'].play(-1)  # Loop indefinitely
    
    def reset_game(self):
        """Reset the game to its initial state"""
        self.player = Player(self.assets)
        self.enemies = []
        self.bullets = []
        self.powerups = []
        
        # Game variables
        self.score = 0
        self.last_enemy_spawn = 0
        self.last_difficulty_increase = 0
        self.last_survival_bonus = 0
        self.enemy_speed_multiplier = 1.0
        self.game_over = False
        
        # Spawn initial enemies
        for _ in range(5):
            self.spawn_enemy()
    
    def init_ui(self):
        """Initialize UI elements"""
        # Fonts
        self.main_font = self.assets['main_font']
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # UI elements
        self.health_bar = HealthBar(SCREEN_WIDTH - 150, 20, 130, 20, PLAYER_LIVES)
        self.score_display = ScoreDisplay(20, 20, self.main_font)
        self.lives_display = LivesDisplay(20, 60, self.small_font, self.assets['player_ship'])
        self.powerup_indicator = PowerupIndicator(SCREEN_WIDTH - 200, 50, self.small_font)
        
        # Menu buttons
        button_width, button_height = 200, 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.menu_buttons = [
            Button(center_x, 200, button_width, button_height, "Start Game", self.main_font, STATE_GAMEPLAY),
            Button(center_x, 270, button_width, button_height, "Instructions", self.main_font, STATE_INSTRUCTIONS),
            Button(center_x, 340, button_width, button_height, "Settings", self.main_font, STATE_SETTINGS),
            Button(center_x, 410, button_width, button_height, "Quit", self.main_font, "quit")
        ]
        
        self.pause_buttons = [
            Button(center_x, 200, button_width, button_height, "Resume", self.main_font, STATE_GAMEPLAY),
            Button(center_x, 270, button_width, button_height, "Main Menu", self.main_font, STATE_MENU),
            Button(center_x, 340, button_width, button_height, "Quit", self.main_font, "quit")
        ]
        
        self.game_over_buttons = [
            Button(center_x, 300, button_width, button_height, "Retry", self.main_font, "retry"),
            Button(center_x, 370, button_width, button_height, "Main Menu", self.main_font, STATE_MENU),
            Button(center_x, 440, button_width, button_height, "Quit", self.main_font, "quit")
        ]
        
        self.instruction_buttons = [
            Button(center_x, 500, button_width, button_height, "Back", self.main_font, STATE_MENU)
        ]
        
        self.settings_buttons = [
            Button(center_x, 500, button_width, button_height, "Back", self.main_font, STATE_MENU)
        ]
    
    def spawn_enemy(self):
        """Spawn a new enemy"""
        enemy = Enemy(self.assets)
        # Apply difficulty scaling to enemy speed
        enemy.speed_y *= self.enemy_speed_multiplier
        self.enemies.append(enemy)
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == STATE_GAMEPLAY:
                        self.state = STATE_PAUSE
                    elif self.state == STATE_PAUSE:
                        self.state = STATE_GAMEPLAY
                
                if event.key == pygame.K_p and self.state == STATE_GAMEPLAY:
                    self.state = STATE_PAUSE
                
                if event.key == pygame.K_m:
                    # Toggle music
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            
            # Handle player input in gameplay state
            if self.state == STATE_GAMEPLAY:
                self.player.handle_input(event)
            
            # Handle button clicks
            mouse_pos = pygame.mouse.get_pos()
            
            if self.state == STATE_MENU:
                for button in self.menu_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        if action == "quit":
                            self.quit_game()
                        else:
                            self.state = action
            
            elif self.state == STATE_PAUSE:
                for button in self.pause_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        if action == "quit":
                            self.quit_game()
                        else:
                            self.state = action
            
            elif self.state == STATE_GAME_OVER:
                for button in self.game_over_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        if action == "quit":
                            self.quit_game()
                        elif action == "retry":
                            self.reset_game()
                            self.state = STATE_GAMEPLAY
                        else:
                            self.state = action
            
            elif self.state == STATE_INSTRUCTIONS:
                for button in self.instruction_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        self.state = action
            
            elif self.state == STATE_SETTINGS:
                for button in self.settings_buttons:
                    button.update(mouse_pos)
                    action = button.handle_event(event)
                    if action:
                        self.state = action
    
    def update_gameplay(self):
        """Update game objects during gameplay"""
        current_time = pygame.time.get_ticks()
        
        # Update player
        self.player.update()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Respawn enemies that go off screen
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.spawn_enemy()
        
        # Update powerups
        for powerup in self.powerups[:]:
            if powerup.update():
                self.powerups.remove(powerup)
        
        # Check collisions
        collision_results = check_collisions(self.player, self.enemies, self.bullets, self.powerups)
        
        # Handle enemy destruction
        for enemy in collision_results['enemies_destroyed']:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
                
                # Create floating score text
                self.floating_texts.append(
                    create_floating_text(f"+{SCORE_ASTEROID_DESTROYED}", 
                                        (enemy.rect.centerx, enemy.rect.centery))
                )
                
                # Chance to spawn powerup
                powerup = spawn_random_powerup(enemy.rect.centerx, enemy.rect.centery, self.assets)
                if powerup:
                    self.powerups.append(powerup)
                
                # Spawn a new enemy
                self.spawn_enemy()
        
        # Handle bullet removal
        for bullet in collision_results['bullets_to_remove']:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        
        # Handle powerup collection
        if collision_results['powerup_collected']:
            powerup = collision_results['powerup_collected']
            if powerup in self.powerups:
                powerup.apply(self.player)
                self.powerups.remove(powerup)
                
                # Create floating score text
                self.floating_texts.append(
                    create_floating_text(f"+{SCORE_POWERUP_COLLECTED}", 
                                        (self.player.rect.centerx, self.player.rect.top),
                                        color=PURPLE)
                )
        
        # Handle player hit
        if collision_results['player_hit']:
            self.player.hit()
            
            # Create floating score text
            self.floating_texts.append(
                create_floating_text(f"{SCORE_HIT_PENALTY}", 
                                    (self.player.rect.centerx, self.player.rect.top),
                                    color=RED)
            )
            
            # Check for game over
            if self.player.is_dead():
                self.state = STATE_GAME_OVER
        
        # Update score
        self.score += collision_results['score_change']
        
        # Spawn enemies
        if len(self.enemies) < MAX_ENEMIES and current_time - self.last_enemy_spawn > ENEMY_SPAWN_RATE:
            self.last_enemy_spawn = current_time
            self.spawn_enemy()
        
        # Increase difficulty over time
        if current_time - self.last_difficulty_increase > ENEMY_SPEED_INCREASE_INTERVAL:
            self.last_difficulty_increase = current_time
            self.enemy_speed_multiplier += ENEMY_SPEED_INCREASE_AMOUNT
            
            # Apply to existing enemies
            for enemy in self.enemies:
                enemy.speed_y *= 1.1
        
        # Award survival bonus
        if current_time - self.last_survival_bonus > SCORE_SURVIVAL_INTERVAL:
            self.last_survival_bonus = current_time
            self.score += SCORE_SURVIVAL_BONUS
            
            # Create floating score text
            self.floating_texts.append(
                create_floating_text(f"+{SCORE_SURVIVAL_BONUS} Survival Bonus!", 
                                    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                    color=GREEN,
                                    size=30,
                                    duration=2000)
            )
        
        # Update floating texts
        update_floating_texts(self.floating_texts)
        
        # Update UI elements
        self.health_bar.update(self.player.lives)
        self.score_display.update(self.score)
        self.lives_display.update(self.player.lives)
        self.powerup_indicator.update(self.player)
        
        # Handle player shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            new_bullets = self.player.shoot()
            if new_bullets:
                self.bullets.extend(new_bullets)
    
    def update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()
        
        # Handle different game states
        if self.state == STATE_SPLASH:
            # Show splash screen for a few seconds
            if current_time - self.splash_start_time > 3000:  # 3 seconds
                self.state = STATE_MENU
        
        elif self.state == STATE_GAMEPLAY:
            self.update_gameplay()
        
        # Update background scrolling
        self.bg_y = (self.bg_y + 1) % SCREEN_HEIGHT
    
    def render_splash_screen(self):
        """Render the splash screen"""
        self.screen.fill(BLACK)
        
        # Draw logo
        logo_text = self.large_font.render("ASTRO SPACE", True, NEON_BLUE)
        logo_rect = logo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(logo_text, logo_rect)
        
        # Draw loading text
        loading_text = self.small_font.render("Loading...", True, WHITE)
        loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(loading_text, loading_rect)
    
    def render_menu(self):
        """Render the main menu"""
        # Draw scrolling background
        self.screen.blit(self.assets['background'], (0, self.bg_y))
        self.screen.blit(self.assets['background'], (0, self.bg_y - SCREEN_HEIGHT))
        
        # Draw title
        title_text = self.large_font.render("ASTRO SPACE", True, NEON_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.menu_buttons:
            button.draw(self.screen)
    
    def render_gameplay(self):
        """Render the gameplay screen"""
        # Draw scrolling background
        self.screen.blit(self.assets['background'], (0, self.bg_y))
        self.screen.blit(self.assets['background'], (0, self.bg_y - SCREEN_HEIGHT))
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw UI elements
        self.health_bar.draw(self.screen)
        self.score_display.draw(self.screen)
        self.lives_display.draw(self.screen)
        self.powerup_indicator.draw(self.screen)
        
        # Draw floating texts
        draw_floating_texts(self.screen, self.floating_texts, self.small_font)
    
    def render_pause(self):
        """Render the pause menu"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_text = self.large_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(pause_text, pause_rect)
        
        # Draw buttons
        for button in self.pause_buttons:
            button.draw(self.screen)
    
    def render_game_over(self):
        """Render the game over screen"""
        # Fade to black
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.large_font.render("MISSION FAILED", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Draw final score
        score_text = self.main_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(score_text, score_rect)
        
        # Draw buttons
        for button in self.game_over_buttons:
            button.draw(self.screen)
    
    def render_instructions(self):
        """Render the instructions screen"""
        self.screen.fill(BLACK)
        
        # Draw title
        title_text = self.large_font.render("INSTRUCTIONS", True, NEON_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw instructions
        instructions = [
            "Controls:",
            "- Arrow keys or WASD: Move ship",
            "- Space: Fire bullet",
            "- P: Pause game",
            "- M: Mute sound",
            "",
            "Objective:",
            "- Destroy asteroids to earn points",
            "- Avoid collisions with asteroids",
            "- Collect power-ups for special abilities",
            "",
            "Power-ups:",
            "- Double Shot (Purple): Fire two bullets at once",
            "- Shield (Blue): Temporary invincibility",
            "- Speed Boost (Yellow): Increased movement speed",
            "- Extra Life (Red): Gain an additional life"
        ]
        
        y = 120
        for line in instructions:
            if line == "":
                y += 10
                continue
                
            text = self.small_font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 4, y))
            y += 25
        
        # Draw buttons
        for button in self.instruction_buttons:
            button.draw(self.screen)
    
    def render_settings(self):
        """Render the settings screen"""
        self.screen.fill(BLACK)
        
        # Draw title
        title_text = self.large_font.render("SETTINGS", True, NEON_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw settings text
        settings_text = self.main_font.render("Sound and Music Volume Controls", True, WHITE)
        settings_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(settings_text, settings_rect)
        
        # Draw buttons
        for button in self.settings_buttons:
            button.draw(self.screen)
    
    def render(self):
        """Render the current game state"""
        if self.state == STATE_SPLASH:
            self.render_splash_screen()
        
        elif self.state == STATE_MENU:
            self.render_menu()
        
        elif self.state == STATE_GAMEPLAY:
            self.render_gameplay()
        
        elif self.state == STATE_PAUSE:
            # First render the gameplay screen
            self.render_gameplay()
            # Then render the pause overlay
            self.render_pause()
        
        elif self.state == STATE_GAME_OVER:
            # First render the gameplay screen
            self.render_gameplay()
            # Then render the game over overlay
            self.render_game_over()
        
        elif self.state == STATE_INSTRUCTIONS:
            self.render_instructions()
        
        elif self.state == STATE_SETTINGS:
            self.render_settings()
        
        # Update the display
        pygame.display.flip()
    
    def quit_game(self):
        """Quit the game"""
        pygame.quit()
        sys.exit()
    
    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
