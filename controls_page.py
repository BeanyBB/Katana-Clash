import pygame
import sys

def controls_page(screen, clock, FPS, resource_path):
    """Displays the controls page."""
    controls_bg_color = (30, 30, 30)  # Dark grey background for the controls page
    title_color = (255, 255, 255)  # White for control titles
    value_color = (50, 200, 50)  # Green for control values

    try:
        controls_title_font = pygame.font.Font(resource_path("./fonts/EdoSZ.ttf"), 40)  # Font for control titles
        controls_value_font = pygame.font.Font(resource_path("./fonts/EdoSZ.ttf"), 40)  # Font for control values
    except FileNotFoundError:
        controls_title_font = pygame.font.SysFont("Arial", 40)  # Fallback title font
        controls_value_font = pygame.font.SysFont("Arial", 40)  # Fallback value font

    controls_text = [
        ("Player 1 Controls", ""),
        ("Move Left:", "A"),
        ("Move Right:", "D"),
        ("Jump:", "W"),
        ("Attack:", "Space"),
        ("Defend:", "S"),
        ("", ""),
        ("Player 2 Controls", ""),
        ("Move Left:", "Left Arrow"),
        ("Move Right:", "Right Arrow"),
        ("Jump:", "Up Arrow"),
        ("Attack:", "Enter"),
        ("Defend:", "Down Arrow"),
        ("", ""),
        ("Press ESC to return.", ""),
    ]

    running = True
    while running:
        # Background color
        screen.fill(controls_bg_color)

        # Render controls text
        x_padding_title = 50  # Left padding for titles
        x_padding_value = 300  # Left padding for values
        y_offset = 100  # Vertical starting position
        line_spacing = 50  # Spacing between lines

        for title, value in controls_text:
            if title:  # Render the title
                rendered_title = controls_title_font.render(title, True, title_color)
                screen.blit(rendered_title, (x_padding_title, y_offset))

            if value:  # Render the corresponding value
                rendered_value = controls_value_font.render(value, True, value_color)
                screen.blit(rendered_value, (x_padding_value, y_offset))

            y_offset += line_spacing  # Move down for the next line

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Return to the main menu
                running = False

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)
