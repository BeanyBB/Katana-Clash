# utils.py

import pygame
from settings import WHITE

def draw_text(screen, text, font, color, x, y):
    """Helper function to draw text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_winner(screen, font, text):
    """Display the winner and wait for a few seconds."""
    screen.fill(WHITE)
    label = font.render(text, True, (0, 0, 0))
    screen.blit(label, (400 - label.get_width() // 2, 300 - label.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
