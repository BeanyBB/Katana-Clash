# main.py

import pygame
import sys, os
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GRAY, BLUE, RED, GREEN, FPS,
    GROUND_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT
)
from player import Player
from utils import draw_winner
import asyncio

pygame.init()

def resource_path(relative_path):
    """Get the absolute path to the resource."""
    # When running in a PyInstaller bundle, _MEIPASS stores the temp directory where assets are extracted
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


background_img = pygame.image.load(resource_path("./images/Background.png"))
ground_img = pygame.image.load(resource_path("./images/ground1.png"))
platform_img = pygame.image.load(resource_path("./images/ground2.png"))

background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_img = pygame.transform.scale(ground_img, (SCREEN_WIDTH, GROUND_HEIGHT))
platform_img = pygame.transform.scale(platform_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

# Menu assets
menu_background_img = pygame.image.load(resource_path("./images/mainMenu.jpg"))
menu_logo_img = pygame.image.load(resource_path("./images/logo.png"))
menu_prompt_img = pygame.image.load(resource_path("./images/space.png"))

# Scale menu images to fit the screen
menu_background_img = pygame.transform.scale(menu_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_logo_img = pygame.transform.scale(menu_logo_img, (600, 150))  # Adjust size as needed
menu_prompt_img = pygame.transform.scale(menu_prompt_img, (400, 50))  # Adjust size as needed

def controls_page():
    """Displays the controls page."""
    controls_bg_color = (30, 30, 30)  # Dark grey background for the controls page
    title_color = (255, 255, 255)  # White for control titles
    value_color = (50, 200, 50)  # Green for control values

    try:
        controls_title_font = pygame.font.Font(resource_path("./fonts/EdoSZ.ttf", 40))  # Font for control titles
        controls_value_font = pygame.font.Font(resource_path("./fonts/EdoSZ.ttf", 40))  # Font for control values
    except FileNotFoundError:
        controls_title_font = pygame.font.SysFont("Arial", 40)  # Fallback title font
        controls_value_font = pygame.font.SysFont("Arial", 40)  # Fallback value font

    controls_text = [
        ("Player 1 Controls", ""),
        ("Move Left:", "A"),
        ("Move Right:", "D"),
        ("Jump:", "W"),
        ("Attack:", "Space"),
        ("Defend:", "E"),
        ("", ""),
        ("Player 2 Controls", ""),
        ("Move Left:", "Left Arrow"),
        ("Move Right:", "Right Arrow"),
        ("Jump:", "Up Arrow"),
        ("Attack:", "Enter"),
        ("Defend:", "Left Shift"),
        ("", ""),
        ("Press ESC to return to the main menu.", ""),
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



def main_menu():
    """Main menu screen with characters running in from the sides."""
    # Button colors and text styles
    start_button_color = (34, 87, 51)  # Dark greenish color
    start_hover_color = (47, 120, 71)  # Slightly brighter green for hover
    quit_button_color = (150, 40, 40)  # Dark reddish color
    quit_hover_color = (200, 60, 60)  # Slightly brighter red for hover
    controls_button_color = (100, 100, 100)  # Grey color for controls button
    controls_hover_color = (140, 140, 140)  # Slightly lighter grey for hover
    text_color = (255, 255, 255)  # White text

    # Button dimensions
    start_button_width, start_button_height = 500, 120
    start_button_x = (SCREEN_WIDTH - start_button_width) // 2
    start_button_y = 500  # Positioned lower on the screen

    quit_button_width, quit_button_height = 150, 50
    quit_button_x = SCREEN_WIDTH - quit_button_width - 20  # 20px padding from the right
    quit_button_y = 20  # Positioned near the top

    controls_button_width, controls_button_height = 250, 50
    controls_button_x = 20  # 20px padding from the left
    controls_button_y = 20  # Positioned near the top

    # Load fonts
    try:
        button_font = pygame.font.Font("./fonts/Freedom-10eM.ttf", 60)  # Custom samurai-style font
        small_button_font = pygame.font.Font("./fonts/Freedom-10eM.ttf", 40)  # Smaller font for quit and controls buttons
    except FileNotFoundError:
        button_font = pygame.font.SysFont("Arial", 60)  # Fallback font
        small_button_font = pygame.font.SysFont("Arial", 40)

    # Positions and states for the characters
    player1_x = -PLAYER_WIDTH  # Off-screen to the left
    player2_x = SCREEN_WIDTH  # Off-screen to the right
    player_y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
    stop_distance = 200  # Distance from the screen center where they stop
    player1_target = SCREEN_WIDTH // 2 - stop_distance - PLAYER_WIDTH
    player2_target = SCREEN_WIDTH // 2 + stop_distance

    player_speed = 10  # Speed at which the characters move
    players_stopped = False  # Flag to indicate if both players have stopped

    while True:
        # Render the menu background
        screen.blit(menu_background_img, (0, 0))

        # Draw the logo
        bigger_logo = pygame.transform.scale(menu_logo_img, (900, 250))  # Make the logo larger
        screen.blit(bigger_logo, ((SCREEN_WIDTH - bigger_logo.get_width()) // 2, 150))  # Center the logo

        # Character running animation
        if not players_stopped:
            if player1_x < player1_target:
                player1_x += player_speed
            if player2_x > player2_target:
                player2_x -= player_speed
            if player1_x >= player1_target and player2_x <= player2_target:
                players_stopped = True  # Both players have reached their target positions

        # Draw players
        screen.blit(player1.animations["run"][player1.current_frame], (player1_x, player_y))
        screen.blit(pygame.transform.flip(player2.animations["run"][player2.current_frame], True, False), (player2_x, player_y))

        # Update player animation frames for running
        player1.update_animation(fps=FPS)
        player2.update_animation(fps=FPS)

        # --- Start Button ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovering_start = (
            start_button_x <= mouse_x <= start_button_x + start_button_width
            and start_button_y <= mouse_y <= start_button_y + start_button_height
        )

        # Draw Start button with hover effect
        shadow_color = (25, 65, 39)
        pygame.draw.rect(screen, shadow_color, (start_button_x + 5, start_button_y + 5, start_button_width, start_button_height), border_radius=20)
        pygame.draw.rect(screen, start_hover_color if is_hovering_start else start_button_color, (start_button_x, start_button_y, start_button_width, start_button_height), border_radius=20)

        # Render Start button text
        start_button_text = button_font.render("Start Game", True, text_color)
        start_text_x = start_button_x + (start_button_width - start_button_text.get_width()) // 2
        start_text_y = start_button_y + (start_button_height - start_button_text.get_height()) // 2
        screen.blit(start_button_text, (start_text_x, start_text_y))

        # --- Quit Button ---
        is_hovering_quit = (
            quit_button_x <= mouse_x <= quit_button_x + quit_button_width
            and quit_button_y <= mouse_y <= quit_button_y + quit_button_height
        )

        # Draw Quit button with hover effect
        pygame.draw.rect(screen, quit_hover_color if is_hovering_quit else quit_button_color, (quit_button_x, quit_button_y, quit_button_width, quit_button_height), border_radius=10)

        # Render Quit button text
        quit_button_text = small_button_font.render("Quit", True, text_color)
        quit_text_x = quit_button_x + (quit_button_width - quit_button_text.get_width()) // 2
        quit_text_y = quit_button_y + (quit_button_height - quit_button_text.get_height()) // 2
        screen.blit(quit_button_text, (quit_text_x, quit_text_y))

        # --- Controls Button ---
        is_hovering_controls = (
            controls_button_x <= mouse_x <= controls_button_x + controls_button_width
            and controls_button_y <= mouse_y <= controls_button_y + controls_button_height
        )

        # Draw Controls button with hover effect
        pygame.draw.rect(screen, controls_hover_color if is_hovering_controls else controls_button_color, (controls_button_x, controls_button_y, controls_button_width, controls_button_height), border_radius=10)

        # Render Controls button text
        controls_button_text = small_button_font.render("Controls", True, text_color)
        controls_text_x = controls_button_x + (controls_button_width - controls_button_text.get_width()) // 2
        controls_text_y = controls_button_y + (controls_button_height - controls_button_text.get_height()) // 2
        screen.blit(controls_button_text, (controls_text_x, controls_text_y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_hovering_start and players_stopped:  # Start the game
                    return  # Break out of the menu loop and start the game
                if is_hovering_quit:  # Quit the game
                    pygame.quit()
                    sys.exit()
                if is_hovering_controls:  # Open the controls page
                    controls_page()

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)






# Fullscreen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)  # Fullscreen mode
pygame.display.set_caption("2D Fighting Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Ground and platforms
platforms = [
    {"rect": pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT), "img": ground_img},  # Ground
    {"rect": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT - (250 + GROUND_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT), "img": platform_img},  # Left platform
    {"rect": pygame.Rect((SCREEN_WIDTH * 3) // 4 - PLATFORM_WIDTH, SCREEN_HEIGHT - (350 + GROUND_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT), "img": platform_img},  # Right platform
]

# Players
player1 = Player(
    SCREEN_WIDTH // 4, SCREEN_HEIGHT - (GROUND_HEIGHT + (PLAYER_HEIGHT)), BLUE, "./images/commander"
)
player2 = Player(
    (SCREEN_WIDTH * 3) // 4, SCREEN_HEIGHT - (GROUND_HEIGHT + PLAYER_HEIGHT), RED, "./images/samurai"
)
players = [player1, player2]

# Main game loop
def main_game():
    # Reset player states
    player1.health = 100
    player2.health = 100

    # Reset player positions
    player1.rect.x = SCREEN_WIDTH // 4
    player1.rect.y = SCREEN_HEIGHT - (GROUND_HEIGHT + PLAYER_HEIGHT)
    player2.rect.x = (SCREEN_WIDTH * 3) // 4
    player2.rect.y = SCREEN_HEIGHT - (GROUND_HEIGHT + PLAYER_HEIGHT)

    running = True

    while running:
        screen.blit(background_img, (0, 0))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Sort players for dynamic layering
        players.sort(key=lambda obj: obj.rect.bottom)

        # Player movement
        player1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e)  # Player 1: A/D to move, W to jump
        player2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RSHIFT)  # Player 2: Arrow keys to move and jump

        # Apply gravity
        player1.apply_gravity()
        player2.apply_gravity()

        # Check collisions with platforms
        player1.check_collision_with_platforms([platform["rect"] for platform in platforms])
        player2.check_collision_with_platforms([platform["rect"] for platform in platforms])

        # Player attacks
        if keys[pygame.K_SPACE]:  # Player 1 attack
            player1.attack(player2)
        if keys[pygame.K_RETURN]:  # Player 2 attack
            player2.attack(player1)

        # Update animations
        player1.update_animation()
        player2.update_animation()

        # Win condition
        if player1.health <= 0:
            draw_winner(screen, font, "Player 2 Wins!")
            pygame.time.delay(3000)  # Pause for 3 seconds
            return  # Exit the game loop and return to the main menu
        if player2.health <= 0:
            draw_winner(screen, font, "Player 1 Wins!")
            pygame.time.delay(3000)  # Pause for 3 seconds
            return  # Exit the game loop and return to the main menu

        # Draw platforms
        for platform in platforms:
            screen.blit(platform["img"], (platform["rect"].x, platform["rect"].y))

        # Draw players and health bars
        for player in players:
            player.draw(screen)
        player1.draw_health_bar(screen, 30, 30)
        player2.draw_health_bar(screen, SCREEN_WIDTH - 330, 30)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        main_menu()
        main_game()
