import pygame
import sys
from controls_page import controls_page

def main_menu(screen, clock, FPS, resource_path, menu_background_img, menu_logo_img, player1, player2):
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
    start_button_x = (screen.get_width() - start_button_width) // 2
    start_button_y = 500

    quit_button_width, quit_button_height = 150, 50
    quit_button_x = screen.get_width() - quit_button_width - 20  # 20px padding from the right
    quit_button_y = 20  # Positioned near the top

    controls_button_width, controls_button_height = 250, 50
    controls_button_x = 20  # 20px padding from the left
    controls_button_y = 20  # Positioned near the top

    # Load fonts
    try:
        button_font = pygame.font.Font(resource_path("./fonts/Freedom-10eM.ttf"), 60)
        small_button_font = pygame.font.Font(resource_path("./fonts/Freedom-10eM.ttf"), 40)
    except FileNotFoundError:
        button_font = pygame.font.SysFont("Arial", 60)
        small_button_font = pygame.font.SysFont("Arial", 40)

    # Positions and states for the characters
    player1_x = -player1.rect.width  # Off-screen to the left
    player2_x = screen.get_width()  # Off-screen to the right
    player_y = screen.get_height() - player1.rect.height - 100
    stop_distance = 200  # Distance from the screen center where they stop
    player1_target = screen.get_width() // 2 - stop_distance - player1.rect.width
    player2_target = screen.get_width() // 2 + stop_distance

    player_speed = 10
    players_stopped = False

    running = True
    while running:
        # Render the menu background
        screen.blit(menu_background_img, (0, 0))

        # Draw the logo
        bigger_logo = pygame.transform.scale(menu_logo_img, (900, 250))
        screen.blit(bigger_logo, ((screen.get_width() - bigger_logo.get_width()) // 2, 150))

        # Character running animation
        if not players_stopped:
            if player1_x < player1_target:
                player1_x += player_speed
            if player2_x > player2_target:
                player2_x -= player_speed
            if player1_x >= player1_target and player2_x <= player2_target:
                players_stopped = True

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

        pygame.draw.rect(
            screen,
            start_hover_color if is_hovering_start else start_button_color,
            (start_button_x, start_button_y, start_button_width, start_button_height),
            border_radius=20,
        )

        start_button_text = button_font.render("Start Game", True, text_color)
        start_text_x = start_button_x + (start_button_width - start_button_text.get_width()) // 2
        start_text_y = start_button_y + (start_button_height - start_button_text.get_height()) // 2
        screen.blit(start_button_text, (start_text_x, start_text_y))

        # --- Quit Button ---
        is_hovering_quit = (
            quit_button_x <= mouse_x <= quit_button_x + quit_button_width
            and quit_button_y <= mouse_y <= quit_button_y + quit_button_height
        )

        pygame.draw.rect(
            screen,
            quit_hover_color if is_hovering_quit else quit_button_color,
            (quit_button_x, quit_button_y, quit_button_width, quit_button_height),
            border_radius=10,
        )

        quit_button_text = small_button_font.render("Quit", True, text_color)
        quit_text_x = quit_button_x + (quit_button_width - quit_button_text.get_width()) // 2
        quit_text_y = quit_button_y + (quit_button_height - quit_button_text.get_height()) // 2
        screen.blit(quit_button_text, (quit_text_x, quit_text_y))

        # --- Controls Button ---
        is_hovering_controls = (
            controls_button_x <= mouse_x <= controls_button_x + controls_button_width
            and controls_button_y <= mouse_y <= controls_button_y + controls_button_height
        )

        pygame.draw.rect(
            screen,
            controls_hover_color if is_hovering_controls else controls_button_color,
            (controls_button_x, controls_button_y, controls_button_width, controls_button_height),
            border_radius=10,
        )

        controls_button_text = small_button_font.render("Controls", True, text_color)
        controls_text_x = controls_button_x + (controls_button_width - controls_button_text.get_width()) // 2
        controls_text_y = controls_button_y + (controls_button_height - controls_button_text.get_height()) // 2
        screen.blit(controls_button_text, (controls_text_x, controls_text_y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_hovering_start and players_stopped:
                    return
                if is_hovering_quit:
                    pygame.quit()
                    sys.exit()
                if is_hovering_controls:
                    controls_page(screen, clock, FPS, resource_path)

        pygame.display.flip()
        clock.tick(FPS)
