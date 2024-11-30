import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_text(screen, text, font, color, x, y):
    """Helper function to draw text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_winner(screen, font, text, player, background_img):
    """
    Cinematic winning screen:
    - Darkness closes in from all sides toward the player.
    - Darkness stops at a fixed distance around the player, creating a spotlight effect.
    - Winning text fades in after the darkness animation finishes.
    """
    clock = pygame.time.Clock()
    FPS = 60

    # Darkness rectangle settings
    darkness_alpha = 180  # Transparency level of the darkness (0 = fully transparent, 255 = fully opaque)
    circle_radius = 0  # Starting radius for the illuminated area around the player
    max_radius = 200  # Maximum radius for the illuminated circle around the player
    circle_grow_speed = 8  # Speed at which the illuminated circle grows

    # Text animation settings
    text_alpha = 0  # Text starts fully transparent
    text_fade_speed = 5  # Speed at which the text fades in
    text_color = (255, 255, 255)  # White text

    # Center position for the player and light effect
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Reset the player position for the winning screen
    player.rect.x = center_x - player.rect.width // 2
    player.rect.y = center_y - player.rect.height // 2
    player.current_frame = 0  # Reset animation to the first frame

    # Winning text surface
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(center_x, center_y - player.rect.height // 2 - 50))

    running = True
    while running:
        # Draw the main game background
        screen.blit(background_img, (0, 0))

        # Draw the player in the center
        player.draw(screen)

        # Darkness closing in
        if circle_radius < max_radius:
            circle_radius += circle_grow_speed
        else:
            # Stop growing the circle when it reaches the maximum radius
            circle_radius = max_radius

        # Create the darkness effect
        darkness_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(darkness_surface, (0, 0, 0, darkness_alpha), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.circle(darkness_surface, (0, 0, 0, 0), (center_x, center_y), circle_radius)
        screen.blit(darkness_surface, (0, 0))

        # Fade in the winning text
        if circle_radius >= max_radius:
            if text_alpha < 255:
                text_alpha = min(255, text_alpha + text_fade_speed)
            text_surf.set_alpha(text_alpha)
            screen.blit(text_surf, text_rect)

        # Stop the animation when everything is complete
        if circle_radius >= max_radius and text_alpha >= 255:
            pygame.time.wait(3000)  # Pause for 2 seconds
            running = False

        pygame.display.flip()
        clock.tick(FPS)
