# settings.py

import pygame

# Initialize PyGame display info to get fullscreen resolution
pygame.init()
display_info = pygame.display.Info()  # Get the monitor's resolution

# Screen settings
SCREEN_WIDTH = display_info.current_w  # Fullscreen width
SCREEN_HEIGHT = display_info.current_h  # Fullscreen height

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Platform sizes (dynamic based on screen size)
GROUND_HEIGHT = 50  # Ground thickness
PLATFORM_WIDTH = SCREEN_WIDTH // 6  # Dynamic platform width
PLATFORM_HEIGHT = 40  # Platform thickness

# Player sizes
PLAYER_WIDTH = 150  # Width of the player
PLAYER_HEIGHT = 175  # Height of the player

# Game settings
GRAVITY = 1.0  # Increased gravity for bigger players
JUMP_STRENGTH = -20  # Higher jump strength for bigger screen
PLAYER_SPEED = 8  # Faster player movement for bigger screen
ATTACK_DAMAGE = 10

# FPS
FPS = 60

