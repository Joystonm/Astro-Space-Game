# Astro Space Game

A 2D Top-Down Space Shooter featuring arcade-style gameplay, colorful visuals, thrilling enemy waves, power-ups, and immersive sound effects.

## Game Flow

### Screens and Transitions
- **Splash Screen**: A short animation of the Astro Space logo with background music.
- **Main Menu**: Start Game, Instructions, Settings, Quit.
- **Instructions**: Shows controls, game objective, and guide to power-ups.
- **Gameplay Screen**: Main arena where player, enemies, bullets interact.
- **Pause Menu**: Allows resume, return to main menu, or quit.
- **Game Over Screen**: Displays final score and buttons to Retry or Exit.

## Visual Design

### Background
- Use `seamless_space.png` for infinite starfield scroll.
- Layer with `bg_big.png` or `space3.jpg` for parallax effect.

### Sprites
- `ship.png`: Player ship with smooth directional animation.
- `asteroid.png`: Rotates while falling to simulate tumbling in space.
- `bullet.png`: Glowing trail or effect for futuristic shooting.
- `ship_exploded.png`: Fade-out or sprite-sheet explosion on player death.

### UI Design
- **Font**: `simkai.ttf` styled in white or neon blue with drop shadows.
- **Buttons**: Rounded with hover and click color transitions.
- **Score & Lives**: Positioned top-left in digital sci-fi style.
- **Health bar**: Top-right, with smooth transition animations.

## Sound Design

### Background Music
- `Cool Space Music.mp3` plays in both menu and gameplay (looped).

### Sound Effects
- `shot.ogg`: Triggered when the player fires a bullet.
- `boom.wav`: Explosion or asteroid break sound.
- Optional: Add ambient hum or subtle effects for deeper immersion.

### Settings
- Allow sound/music volume control from the Settings screen.

## Core Gameplay Mechanics

### Controls
- **Arrow keys** or **W/A/S/D**: Move ship.
- **Space**: Fire bullet.
- **P**: Pause game.
- **M**: Mute background music and effects.

### Player Mechanics
- Starts with 3 lives.
- Fires bullets at fixed intervals (cooldown).
- Collision with asteroid: lose one life and trigger explosion.

### Enemy (Asteroid) Mechanics
- Spawn from top or at slight angles from left/right.
- Vary in speed and size.
- Appear in increasing frequency as time progresses.

### Collision Detection
- Bullet hits asteroid: Destroy both, add score, play boom sound.
- Asteroid hits player: Reduce life, show explosion, screen shake (optional).

## Power-Ups

Spawn randomly from destroyed asteroids:

| Name | Visual Hint | Effect |
|------|-------------|--------|
| Double Shot | Purple capsule | Fires two bullets simultaneously |
| Shield | Blue orb | Temporary invincibility |
| Speed Boost | Lightning icon | Increases ship movement speed |
| Extra Life | Heart icon | Adds one life to player's count |

## Level Design / Difficulty

Use dynamic difficulty rather than fixed levels:
- Asteroid speed increases every 15 seconds.
- Enemy frequency increases over time.
- Optional: Introduce a "Boss Asteroid" requiring multiple hits.

## Scoring System

| Action | Points |
|--------|--------|
| Destroy an asteroid | +10 |
| Survive every 30 seconds | +50 |
| Collect a power-up | +20 |
| Hit by asteroid | -50 |

- Display score top-left in large neon digital style.
- Optional floating "+10" animations when points are scored.

## UI Elements

### Main Menu
- Animated background with scrolling stars.
- Hover effects and subtle button animations.
- Music starts here and loops.

### Instructions Page
- Styled with `simkai.ttf`.
- Icons next to text (e.g., shield icon beside "Shield").

### Pause Menu
- Dark semi-transparent overlay.
- Centered white "Paused" text with Resume, Main Menu, Quit buttons.

### Game Over Screen
- Fade to black after player loses all lives.
- Show "Mission Failed" or "Victory!" depending on score.
- Final score, Retry and Main Menu buttons shown.

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
│   │   └── bg_big.png
│   └── sounds/
│       ├── Cool Space Music.mp3
│       ├── shot.ogg
│       └── boom.wav
├── main.py
├── player.py
├── enemy.py
├── bullet.py
├── config.py
├── utils.py
└── README.md
```

## Development Status

- [x] Project structure setup
- [x] Basic player movement
- [x] Enemy generation
- [x] Bullet mechanics
- [ ] Collision detection
- [ ] Power-up system
- [ ] UI implementation
- [ ] Sound integration
- [ ] Menu screens
- [ ] Scoring system
