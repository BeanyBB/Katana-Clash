from player import Player
import pygame

def game_loop(screen, clock, running, dt):
    player1 = Player('sword', 'default', 'player1', screen,
                     pygame.Vector2(screen.get_width() / 1.5, screen.get_height() / 2), "red")
    player2 = Player('sword', 'default', 'player1', screen,
                     pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2), "blue")

    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        player1.show_player()
        player2.show_player()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player1.move_left(dt)
        if keys[pygame.K_d]:
            player1.move_right(dt)
        if keys[pygame.K_RIGHT]:
            player2.move_right(dt)
        if keys[pygame.K_LEFT]:
            player2.move_left(dt)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    game_loop(screen, clock, running, dt)



if __name__ == '__main__':
    main()


