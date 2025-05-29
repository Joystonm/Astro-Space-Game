# AstroSpace Game

A 2D space shooter game built with Pygame where players control a spaceship to destroy enemy ships while avoiding collisions.

## Features

- Player-controlled spaceship with movement and shooting abilities
- Enemy ships that spawn randomly and move in patterns
- Collision detection between bullets, player, and enemies
- Score tracking system
- Sound effects and background music
- Explosion animations

## Requirements

- Python 3.6+
- Pygame 2.0+

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python main.py
   ```

## Controls

- Arrow keys: Move the spaceship
- Space: Shoot
- ESC: Quit the game

## Project Structure

```
AstroSpace/
│
├── assets/               # All images, sounds, and fonts
│   ├── images/           # Spaceships, asteroids, stars, etc.
│   ├── sounds/           # Laser shots, explosion, background music
│   └── fonts/            # Custom game fonts
│
├── main.py               # Main game loop and core logic
├── player.py             # Handles player spaceship movement and actions
├── enemy.py              # Enemy logic and spawn behavior
├── bullet.py             # Bullet and collision handling
├── config.py             # Game settings like screen size, speed, etc.
├── utils.py              # Helper functions (e.g., loading assets)
└── README.md             # Project overview and instructions
```

## Adding Custom Assets

To add your own assets to the game:

1. Place image files in the `assets/images/` directory
2. Place sound files in the `assets/sounds/` directory
3. Place font files in the `assets/fonts/` directory
4. Update the file paths in `config.py` to point to your new assets

## Future Improvements

- Add power-ups and special weapons
- Implement different enemy types
- Add levels with increasing difficulty
- Create a high score system
- Add boss battles

## License

This project is licensed under the MIT License - see the LICENSE file for details.
