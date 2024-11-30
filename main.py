# main.py

import pygame
import sys, os
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GRAY, BLUE, RED, GREEN, FPS,
    GROUND_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT
)
from player import Player
from utils import draw_winner
from main_menu import main_menu
from controls_page import controls_page

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

# Fullscreen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)  # Fullscreen mode
pygame.display.set_caption("2D Fighting Game")
clock = pygame.time.Clock()
font = pygame.font.Font(resource_path("./fonts/Freedom-10eM.ttf"), 30)

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
    player1.rect.x = 40
    player1.rect.y = 0
    player2.rect.x = SCREEN_WIDTH - (PLAYER_WIDTH + 40)
    player2.rect.y = 0
    player2.flip = True
    player1.is_jumping = True
    player2.is_jumping = True
    player1.state = 'jump'
    player2.state = 'jump'

    # Disable input initially
    player1.input_allowed = False
    player2.input_allowed = False

    # Load Fight image
    fight_img = pygame.image.load(resource_path("./images/Fight.png"))
    fight_img = pygame.transform.scale(fight_img, (800, 400))  # Scale as needed
    fight_rect = fight_img.get_rect(center=(SCREEN_WIDTH // 2, -200))  # Start above the screen
    # Alpha surface for fading effect
    fight_surface = pygame.Surface(fight_img.get_size(), pygame.SRCALPHA)
    fight_surface.blit(fight_img, (0, 0))
    fight_alpha = 255  # Start fully opaque
    fight_target_y = 300  # Final position (a little toward the top)
    fight_speed = 40  # Initial speed
    fight_animation_done = False
    fight_display_timer = None  # Timer to track the 1-second delay

    # Add a timer to re-enable input (in milliseconds)
    input_enable_time = pygame.time.get_ticks() + 1500  # 1.5 seconds

    # Button settings for Main Menu and Controls
    menu_button_color = (100, 100, 100)  # Grey
    menu_button_hover_color = (140, 140, 140)  # Light Grey
    controls_button_color = (50, 50, 150)  # Dark Blue
    controls_button_hover_color = (80, 80, 200)  # Light Blue

    # Button dimensions
    button_height = 50
    menu_button_width = 220  # Increased by 20 pixels
    controls_button_width = 200
    menu_button_x = 30 + 300 + 20  # To the right of Player 1's health bar
    menu_button_y = 30  # Same Y as Player 1's health bar
    controls_button_x = SCREEN_WIDTH - 330 - controls_button_width - 20  # To the left of Player 2's health bar
    controls_button_y = 30  # Same Y as Player 2's health bar
    menu_button_text = font.render("Main Menu", True, (255, 255, 255))  # White text
    controls_button_text = font.render("Controls", True, (255, 255, 255))  # White text

    running = True
    paused_for_controls = False

    while running:
        # Check if the game is paused for the controls page
        if paused_for_controls:
            controls_page(screen, clock, FPS, resource_path)  # Display the controls page
            paused_for_controls = False  # Resume the game after escaping the controls page

        screen.blit(background_img, (0, 0))

        # Enable input after a certain time
        current_time = pygame.time.get_ticks()

        # --- Fight Animation ---
        if not fight_animation_done:
            # Exponential speed decrease for "rolling" effect
            if fight_rect.centery < fight_target_y:
                fight_speed *= 0.95  # Slightly slower deceleration for quicker descent
                fight_rect.centery += max(1, int(fight_speed))  # Prevent speed from hitting zero

            # Add a delay after reaching the target position
            if fight_rect.centery >= fight_target_y:
                if fight_display_timer is None:  # Start the 1-second timer once the target is reached
                    fight_display_timer = pygame.time.get_ticks()  # Get the current time
                elif pygame.time.get_ticks() - fight_display_timer >= 1000:  # 1-second delay (1000 ms)
                    fight_alpha -= 10  # Start fading out
                    if fight_alpha <= 0:  # Animation is done
                        fight_animation_done = True
                        player1.input_allowed = True
                        player2.input_allowed = True  # Enable input after fade

            # Apply fading effect to the Fight image
            fight_surface.set_alpha(fight_alpha)
            screen.blit(fight_surface, fight_rect)

        if current_time > input_enable_time:
            player1.input_allowed = True
            player2.input_allowed = True

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse input
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Main Menu button click
                if menu_button_x <= mouse_x <= menu_button_x + menu_button_width and menu_button_y <= mouse_y <= menu_button_y + button_height:
                    return  # Exit the game loop and return to the main menu

                # Controls button click
                if controls_button_x <= mouse_x <= controls_button_x + controls_button_width and controls_button_y <= mouse_y <= controls_button_y + button_height:
                    paused_for_controls = True  # Pause the game and show the controls page

        # Sort players for dynamic layering
        players.sort(key=lambda obj: obj.rect.bottom)

        # Player movement (only if input is allowed)
        if player1.input_allowed:
            player1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s)  # Player 1: A/D to move, W to jump
        if player2.input_allowed:
            player2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)  # Player 2: Arrow keys to move and jump

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
            draw_winner(screen, font, "Player 2 Wins!", player2, background_img)
            return  # Exit the game loop and return to the main menu
        if player2.health <= 0:
            draw_winner(screen, font, "Player 1 Wins!", player1, background_img)
            return  # Exit the game loop and return to the main menu

        # Draw platforms
        for platform in platforms:
            screen.blit(platform["img"], (platform["rect"].x, platform["rect"].y))

        # Draw players and health bars
        for player in players:
            player.draw(screen)
        player1.draw_health_bar(screen, 30, 30)  # Player 1 health bar
        player2.draw_health_bar(screen, SCREEN_WIDTH - 330, 30)  # Player 2 health bar

        # --- Main Menu Button ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovering_menu = menu_button_x <= mouse_x <= menu_button_x + menu_button_width and menu_button_y <= mouse_y <= menu_button_y + button_height

        # Draw Main Menu button
        pygame.draw.rect(
            screen,
            menu_button_hover_color if is_hovering_menu else menu_button_color,
            (menu_button_x, menu_button_y, menu_button_width, button_height),
            border_radius=10,
        )
        # Draw Main Menu button text
        menu_text_x = menu_button_x + (menu_button_width - menu_button_text.get_width()) // 2
        menu_text_y = menu_button_y + (button_height - menu_button_text.get_height()) // 2
        screen.blit(menu_button_text, (menu_text_x, menu_text_y))

        # --- Controls Button ---
        is_hovering_controls = controls_button_x <= mouse_x <= controls_button_x + controls_button_width and controls_button_y <= mouse_y <= controls_button_y + button_height

        # Draw Controls button
        pygame.draw.rect(
            screen,
            controls_button_hover_color if is_hovering_controls else controls_button_color,
            (controls_button_x, controls_button_y, controls_button_width, button_height),
            border_radius=10,
        )
        # Draw Controls button text
        controls_text_x = controls_button_x + (controls_button_width - controls_button_text.get_width()) // 2
        controls_text_y = controls_button_y + (button_height - controls_button_text.get_height()) // 2
        screen.blit(controls_button_text, (controls_text_x, controls_text_y))

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)




if __name__ == "__main__":
    while True:
        main_menu(screen, clock, FPS, resource_path, menu_background_img, menu_logo_img, player1, player2)
        main_game()
