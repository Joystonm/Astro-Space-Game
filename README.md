# Astro Space Game

A 2D Top-Down Space Shooter featuring arcade-style gameplay, colorful visuals, thrilling asteroid waves, power-ups, and immersive sound effects.

## Game Flow

### Screens and Transitions
- **Splash Screen**: A short animation of the Astro Space logo with background music.
- **Main Menu**: Start Game, Best Score, Instructions, Settings, Quit.
- **Best Score**: Displays the highest score achieved.
- **Instructions**: Shows controls, game objective, and guide to power-ups.
- **Gameplay Screen**: Main arena where player, asteroids, bullets interact.
- **Pause Menu**: Allows resume, return to main menu, or quit.
- **Game Over Screen**: Displays final score and buttons to Retry or Exit.

## Visual Design

### Background
- `seamless_space.png` for infinite starfield scroll during gameplay.
- `background_menu.jpg` for menu screens with semi-transparent overlays.
- `bg_big.png` and `space3.jpg` available for parallax effects.

### Sprites
- `ship.png`: Player ship with directional movement.
- `asteroid.png`: Rotates while falling to simulate tumbling in space.
- `bullet.png`: Projectile fired by the player.
- `ship_exploded.png`: Used when player is destroyed.

### UI Design
- **Font**: `simkai.ttf` styled in white or neon blue with drop shadows.
- **Buttons**: Rounded with hover and click color transitions.
- **Score**: Positioned top-left in digital sci-fi style.
- **Lives**: Displayed as small ship icons.
- **Health bar**: Top-right, with smooth transition animations.
- **Power-up indicators**: Shows active power-ups and their remaining time.

## Sound Design

### Background Music
- `Cool Space Music.mp3` plays in both menu and gameplay (looped).

### Sound Effects
- `shot.ogg`: Triggered when the player fires a bullet.
- `boom.wav`: Explosion sound when asteroids are destroyed.

## Core Gameplay Mechanics

### Controls
- **Arrow keys** or **W/A/S/D**: Move ship.
- **Space**: Fire bullet (hold for continuous fire).
- **P**: Pause game.
- **M**: Mute background music and effects.

### Player Mechanics
- Starts with 3 lives.
- Fires bullets at fixed intervals (cooldown).
- Collision with asteroid: lose one life and trigger temporary invincibility.

### Asteroid Mechanics
- Spawn from top of screen at random positions.
- Rotate while falling to simulate tumbling in space.
- Vary in speed and movement patterns.
- Appear with increasing frequency as time progresses.

### Collision Detection
- Bullet hits asteroid: Destroy both, add score, play boom sound.
- Asteroid hits player: Reduce life, trigger invincibility, subtract points.

## Power-Ups

Spawn randomly from destroyed asteroids:

| Name | Visual Hint | Effect |
|------|-------------|--------|
| Double Shot | Purple square | Fires two bullets simultaneously |
| Shield | Blue square | Temporary invincibility |
| Speed Boost | Yellow square | Increases ship movement speed |
| Extra Life | Red square | Adds one life to player's count |

## Level Design / Difficulty

Dynamic difficulty system:
- Asteroid speed increases every 15 seconds.
- Enemy frequency increases over time.
- Score increases as you destroy more asteroids.

## Scoring System

| Action | Points |
|--------|--------|
| Destroy an asteroid | +10 |
| Survive every 30 seconds | +50 |
| Collect a power-up | +20 |
| Hit by asteroid | -50 |

- Score cannot go below zero.
- High score is saved between game sessions.
- Floating score text animations when points are gained or lost.

## UI Elements

### Main Menu
- Background image with title.
- Buttons for Start Game, Best Score, Instructions, Settings, and Quit.
- Music starts here and loops.

### Best Score Screen
- Displays the highest score achieved.
- Back button to return to main menu.

### Instructions Page
- Shows controls and game mechanics.
- Explains power-ups and scoring system.

### Pause Menu
- Dark semi-transparent overlay.
- Centered "Paused" text with Resume, Main Menu, Quit buttons.

### Game Over Screen
- Fade to black after player loses all lives.
- Shows "Mission Failed" or "New High Score!" depending on score.
- Displays final score and best score.
- Retry and Main Menu buttons.

## Project Structure

```
AstroSpace/
├── assets/
│   ├── fonts/
│   │   └── simkai.ttf
│   ├── images/
│   │   ├── ship.png
│   │   ├── asteroid.png
│   │   ├── bullet.png
│   │   ├── ship_exploded.png
│   │   ├── seamless_space.png
│   │   ├── background_menu.jpg
│   │   ├── bg_big.png
│   │   └── space3.jpg
│   └── sounds/
│       ├── Cool Space Music.mp3
│       ├── shot.ogg
│       └── boom.wav
├── main.py
├── player.py
├── enemy.py
├── bullet.py
├── powerup.py
├── ui.py
├── config.py
├── utils.py
└── README.md
```

## Development Status

- [x] Project structure setup
- [x] Basic player movement
- [x] Asteroid generation
- [x] Bullet mechanics
- [x] Collision detection
- [x] Power-up system
- [x] UI implementation
- [x] Sound integration
- [x] Menu screens
- [x] Scoring system
- [x] High score tracking
- [ ] Additional power-up graphics
- [ ] Screen shake effects
- [ ] Boss asteroids
